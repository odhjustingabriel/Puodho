from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Category, Order, Product, ProductOption


class PuodhoSiteTests(TestCase):
    def setUp(self):
        poultry = Category.objects.create(name='Poultry')
        eggs_category = Category.objects.create(name='Eggs')
        self.broiler = Product.objects.create(
            category=poultry,
            name='Broiler Chicken',
            slug='broiler-chicken',
            description='Farm raised broiler chicken.',
            unit='whole chicken',
            base_price=Decimal('650.00'),
        )
        self.alive = ProductOption.objects.create(product=self.broiler, name='Alive', price=Decimal('650.00'))
        ProductOption.objects.create(product=self.broiler, name='Prepared', price=Decimal('750.00'))
        self.eggs = Product.objects.create(
            category=eggs_category,
            name='Eggs',
            slug='eggs',
            description='Fresh eggs by the tray.',
            unit='tray',
            base_price=Decimal('450.00'),
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fresh poultry')

    def test_products_page_loads(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Broiler Chicken')

    def test_order_page_loads(self):
        response = self.client.get(reverse('order_assistant'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order assistant')

    def test_delivery_method_choices_do_not_include_blank_option(self):
        response = self.client.get(reverse('order_assistant'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(list(form.fields['delivery_method'].choices), Order.DELIVERY_CHOICES)
        self.assertNotContains(response, '---------')

    def test_customer_can_submit_valid_order_and_total_is_calculated(self):
        response = self.client.post(reverse('order_assistant'), {
            'customer_name': 'Achieng Otieno',
            'phone': '0712345678',
            'email': '',
            'location': 'Nearby village',
            'delivery_method': 'delivery',
            'preferred_date': (date.today() + timedelta(days=1)).isoformat(),
            'notes': 'Call before delivery.',
            'selected_products': ['broiler-chicken', 'eggs'],
            'broiler_option': str(self.alive.pk),
            'broiler_quantity': '2',
            'eggs_quantity': '3',
        })
        order = Order.objects.get()
        self.assertRedirects(response, reverse('order_success', kwargs={'reference': order.order_reference}))
        self.assertEqual(order.order_reference, 'PUODHO-1001')
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.total_amount, Decimal('2650.00'))


    def test_cannot_submit_order_with_past_preferred_date(self):
        response = self.client.post(reverse('order_assistant'), {
            'customer_name': 'Achieng Otieno',
            'phone': '0712345678',
            'email': '',
            'location': 'Nearby village',
            'delivery_method': 'delivery',
            'preferred_date': (date.today() - timedelta(days=1)).isoformat(),
            'notes': '',
            'selected_products': ['eggs'],
            'eggs_quantity': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Preferred date cannot be in the past.')
        self.assertEqual(Order.objects.count(), 0)

    def test_seed_command_adds_expanded_catalog(self):
        call_command('seed_puodho')
        self.assertTrue(Product.objects.filter(slug='cattle', options__name__icontains='Sahiwal').exists())
        self.assertTrue(Product.objects.filter(slug='goats', options__name='Boer goat').exists())
        self.assertTrue(Product.objects.filter(slug='sheep', options__name='Dorper sheep').exists())
        self.assertTrue(Product.objects.filter(slug='cow-milk', base_price=Decimal('60.00')).exists())
        self.assertTrue(Product.objects.filter(slug='bulk-milk-order', options__price=Decimal('0.00')).exists())

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_staff_user_can_access_dashboard(self):
        staff = User.objects.create_user(username='staff', password='pass12345', is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
