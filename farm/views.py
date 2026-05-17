from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import OrderAssistantForm, OrderStatusForm, ProductForm, ProductOptionFormSet
from .models import Order, OrderItem, Product


def staff_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func))


def active_products():
    return Product.objects.filter(is_active=True).select_related('category').prefetch_related('options')


def home(request):
    featured_products = active_products()[:3]
    return render(request, 'farm/home.html', {'featured_products': featured_products})


def products(request):
    return render(request, 'farm/products.html', {'products': active_products()})


def order_product_fields(form):
    fields = []
    for product in form.orderable_products:
        quantity_field = form[form.quantity_field_name(product)]
        option_name = form.option_field_name(product)
        fields.append({
            'product': product,
            'quantity_field': quantity_field,
            'option_field': form[option_name] if option_name in form.fields else None,
        })
    return fields


@transaction.atomic
def order_assistant(request):
    if request.method == 'POST':
        form = OrderAssistantForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = Order.PENDING
            order.save()
            for product_id in form.cleaned_data['selected_products']:
                product = form.products_by_id[str(product_id)]
                quantity = form.cleaned_data[form.quantity_field_name(product)]
                option_field = form.option_field_name(product)
                option = form.cleaned_data.get(option_field) if option_field in form.fields else None
                unit_price = option.price if option else product.base_price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_option=option,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=unit_price * quantity,
                )
            return redirect(reverse('order_success', kwargs={'reference': order.order_reference}))
    else:
        form = OrderAssistantForm()
    return render(request, 'farm/order.html', {'form': form, 'order_product_fields': order_product_fields(form)})


def order_success(request, reference):
    order = get_object_or_404(Order.objects.prefetch_related('items__product', 'items__product_option'), order_reference=reference)
    return render(request, 'farm/order_success.html', {'order': order})


def about(request):
    return render(request, 'farm/about.html')


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you. Puodho will review your message and contact you soon.')
        return redirect('contact')
    return render(request, 'farm/contact.html')


@staff_required
def dashboard_home(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.PENDING).count()
    recent_orders = Order.objects.prefetch_related('items').order_by('-created_at')[:8]
    status_counts = Order.objects.values('status').annotate(total=Count('id'))
    return render(request, 'farm/dashboard/home.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'status_counts': status_counts,
    })


@staff_required
def dashboard_orders(request):
    status = request.GET.get('status')
    orders = Order.objects.prefetch_related('items').order_by('-created_at')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'farm/dashboard/orders.html', {
        'orders': orders,
        'status': status,
        'status_choices': Order.STATUS_CHOICES,
    })


@staff_required
def dashboard_order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product', 'items__product_option'), pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'{order.order_reference} updated.')
            return redirect('dashboard_order_detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'farm/dashboard/order_detail.html', {'order': order, 'form': form})


@staff_required
def dashboard_products(request):
    return render(request, 'farm/dashboard/products.html', {'products': Product.objects.select_related('category').prefetch_related('options')})


@staff_required
def dashboard_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            formset = ProductOptionFormSet(request.POST, instance=product)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Product created.')
                return redirect('dashboard_products')
        else:
            formset = ProductOptionFormSet(request.POST)
    else:
        form = ProductForm()
        formset = ProductOptionFormSet()
    return render(request, 'farm/dashboard/product_form.html', {'form': form, 'formset': formset, 'title': 'Add Product'})


@staff_required
def dashboard_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductOptionFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Product updated.')
            return redirect('dashboard_products')
    else:
        form = ProductForm(instance=product)
        formset = ProductOptionFormSet(instance=product)
    return render(request, 'farm/dashboard/product_form.html', {'form': form, 'formset': formset, 'title': 'Edit Product'})
