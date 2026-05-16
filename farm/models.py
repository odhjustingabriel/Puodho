from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    AVAILABLE = 'available'
    LIMITED = 'limited'
    UNAVAILABLE = 'unavailable'
    AVAILABILITY_CHOICES = [
        (AVAILABLE, 'Available'),
        (LIMITED, 'Limited'),
        (UNAVAILABLE, 'Unavailable'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField()
    unit = models.CharField(max_length=80)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default=AVAILABLE)
    stock_quantity = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def can_order(self):
        return self.is_active and self.availability_status != self.UNAVAILABLE

    def __str__(self):
        return self.name


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['product__name', 'price']
        unique_together = ('product', 'name')

    def __str__(self):
        return f'{self.product.name} - {self.name}'


class Order(models.Model):
    PICKUP = 'pickup'
    DELIVERY = 'delivery'
    DELIVERY_CHOICES = [(PICKUP, 'Pickup'), (DELIVERY, 'Delivery')]

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PREPARING = 'preparing'
    READY = 'ready_for_pickup'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (PREPARING, 'Preparing'),
        (READY, 'Ready for Pickup'),
        (OUT_FOR_DELIVERY, 'Out for Delivery'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    ]

    order_reference = models.CharField(max_length=30, unique=True, blank=True)
    customer_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=220)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    preferred_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_reference:
            self.order_reference = f'PUODHO-{1000 + self.pk}'
            super().save(update_fields=['order_reference'])

    @property
    def total_amount(self):
        total = sum((item.line_total for item in self.items.all()), Decimal('0.00'))
        return total

    def __str__(self):
        return self.order_reference or f'Order {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_option = models.ForeignKey(ProductOption, on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be positive.')
        if self.product_option and self.product_option.product_id != self.product_id:
            raise ValidationError('Selected option does not belong to this product.')

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be positive.')
        if self.unit_price is None:
            self.unit_price = self.product_option.price if self.product_option else self.product.base_price
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
