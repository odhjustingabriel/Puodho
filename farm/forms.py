from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Order, Product, ProductOption


class OrderAssistantForm(forms.ModelForm):
    selected_products = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    broiler_quantity = forms.IntegerField(required=False, min_value=1)
    broiler_option = forms.ModelChoiceField(
        queryset=ProductOption.objects.none(),
        required=False,
        widget=forms.RadioSelect,
        empty_label=None,
    )
    eggs_quantity = forms.IntegerField(required=False, min_value=1)

    class Meta:
        model = Order
        fields = [
            'customer_name', 'phone', 'email', 'location', 'delivery_method',
            'preferred_date', 'notes', 'selected_products', 'broiler_quantity',
            'broiler_option', 'eggs_quantity'
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
        products = Product.objects.filter(is_active=True).exclude(availability_status=Product.UNAVAILABLE)
        self.fields['selected_products'].choices = [(p.slug, p.name) for p in products]
        broiler = Product.objects.filter(slug='broiler-chicken').first()
        if broiler:
            self.fields['broiler_option'].queryset = broiler.options.filter(is_active=True)

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < timezone.localdate():
            raise ValidationError('Preferred date cannot be in the past.')
        return preferred_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError('Phone number is required so the farm can confirm your order.')
        return phone

    def clean(self):
        cleaned = super().clean()
        selected = cleaned.get('selected_products') or []
        if 'broiler-chicken' in selected:
            if not cleaned.get('broiler_quantity'):
                self.add_error('broiler_quantity', 'Enter a broiler chicken quantity.')
            if not cleaned.get('broiler_option'):
                self.add_error('broiler_option', 'Choose Alive or Prepared for broiler chicken.')
        if 'eggs' in selected and not cleaned.get('eggs_quantity'):
            self.add_error('eggs_quantity', 'Enter an eggs quantity.')
        if not selected:
            self.add_error('selected_products', 'Choose at least one product.')
        return cleaned


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
