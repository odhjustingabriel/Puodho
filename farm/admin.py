from django.contrib import admin
from .models import Category, Order, OrderItem, Product, ProductOption


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'unit', 'availability_status', 'is_active')
    list_filter = ('category', 'availability_status', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductOptionInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('line_total',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_reference', 'customer_name', 'phone', 'delivery_method', 'status', 'created_at')
    list_filter = ('status', 'delivery_method', 'created_at')
    search_fields = ('order_reference', 'customer_name', 'phone', 'location')
    readonly_fields = ('order_reference', 'created_at', 'updated_at')
    inlines = [OrderItemInline]


admin.site.register(Category)
