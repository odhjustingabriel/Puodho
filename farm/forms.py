from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Order, Product, ProductOption


class OrderAssistantForm(forms.ModelForm):
    selected_products = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Order
        fields = [
            'customer_name', 'phone', 'email', 'location', 'delivery_method',
            'preferred_date', 'notes', 'selected_products'
        ]
        widgets = {
            'delivery_method': forms.RadioSelect(),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferred_date'].widget.attrs['min'] = timezone.localdate().isoformat()
        self.fields['delivery_method'].choices = Order.DELIVERY_CHOICES
        self.orderable_products = list(
            Product.objects.filter(is_active=True)
            .exclude(availability_status=Product.UNAVAILABLE)
            .select_related('category')
            .prefetch_related('options')
            .order_by('category__name', 'name')
        )
        self.products_by_id = {str(product.pk): product for product in self.orderable_products}
        self.fields['selected_products'].choices = [(str(product.pk), product.name) for product in self.orderable_products]

        for product in self.orderable_products:
            quantity_field = self.quantity_field_name(product)
            self.fields[quantity_field] = forms.IntegerField(
                required=False,
                min_value=1,
                label=f'{product.name} quantity',
                widget=forms.NumberInput(attrs={'min': 1}),
            )
            options = product.options.filter(is_active=True)
            if options.exists():
                option_field = self.option_field_name(product)
                self.fields[option_field] = forms.ModelChoiceField(
                    queryset=options,
                    required=False,
                    widget=forms.RadioSelect(),
                    empty_label=None,
                    label=f'{product.name} option',
                )

    @staticmethod
    def quantity_field_name(product):
        return f'product_{product.pk}_quantity'

    @staticmethod
    def option_field_name(product):
        return f'product_{product.pk}_option'

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < timezone.localdate():
            raise ValidationError('Preferred date cannot be in the past.')
        return preferred_date

    def clean_customer_name(self):
        return self.cleaned_data.get('customer_name', '').strip()[:160]

    def clean_location(self):
        return self.cleaned_data.get('location', '').strip()[:220]

    def clean_notes(self):
        return self.cleaned_data.get('notes', '').strip()[:2000]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError('Phone number is required so the farm can confirm your order.')
        if len(phone) > 40:
            raise ValidationError('Phone number is too long.')
        RegexValidator(r'^[0-9+()\-\s]{7,40}$', 'Enter a valid phone number.')(phone)
        return phone

    def clean(self):
        cleaned = super().clean()
        selected = cleaned.get('selected_products') or []
        if not selected:
            self.add_error('selected_products', 'Choose at least one product.')
            return cleaned

        for product_id in selected:
            product = self.products_by_id.get(str(product_id))
            if not product:
                self.add_error('selected_products', 'One of the selected products is no longer available.')
                continue

            quantity_field = self.quantity_field_name(product)
            if not cleaned.get(quantity_field):
                self.add_error(quantity_field, f'Enter a quantity for {product.name}.')

            option_field = self.option_field_name(product)
            if option_field in self.fields and not cleaned.get(option_field):
                self.add_error(option_field, f'Choose an option for {product.name}.')
        return cleaned



class ContactInquiryForm(forms.Form):
    name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=40, validators=[RegexValidator(r'^[0-9+()\-\s]{7,40}$', 'Enter a valid phone number.')])
    message = forms.CharField(max_length=1500, widget=forms.Textarea(attrs={'rows': 5}))

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_phone(self):
        return self.cleaned_data['phone'].strip()

    def clean_message(self):
        return self.cleaned_data['message'].strip()


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'admin_note']
        widgets = {'admin_note': forms.Textarea(attrs={'rows': 4})}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 'unit', 'base_price', 'image',
            'availability_status', 'stock_quantity', 'is_active'
        ]


ProductOptionFormSet = inlineformset_factory(
    Product,
    ProductOption,
    fields=['name', 'price', 'description', 'is_active'],
    extra=1,
    can_delete=True,
)
