from django.core.management.base import BaseCommand
from farm.models import Category, Product, ProductOption


class Command(BaseCommand):
    help = 'Seed Puodho with initial poultry and egg products.'

    def handle(self, *args, **options):
        poultry, _ = Category.objects.get_or_create(
            name='Poultry', defaults={'description': 'Fresh broiler chickens and poultry produce.'}
        )
        eggs_category, _ = Category.objects.get_or_create(
            name='Eggs', defaults={'description': 'Farm fresh eggs sold by the tray.'}
        )
        broiler, _ = Product.objects.update_or_create(
            slug='broiler-chicken',
            defaults={
                'category': poultry,
                'name': 'Broiler Chicken',
                'description': 'Healthy farm-raised broiler chickens available alive or prepared for your kitchen.',
                'unit': 'whole chicken',
                'base_price': 650,
                'availability_status': Product.AVAILABLE,
                'is_active': True,
            },
        )
        ProductOption.objects.update_or_create(
            product=broiler, name='Alive',
            defaults={'price': 650, 'description': 'Live broiler chicken.', 'is_active': True},
        )
        ProductOption.objects.update_or_create(
            product=broiler, name='Prepared',
            defaults={'price': 750, 'description': 'Slaughtered and skinned broiler chicken.', 'is_active': True},
        )
        Product.objects.update_or_create(
            slug='eggs',
            defaults={
                'category': eggs_category,
                'name': 'Eggs',
                'description': 'Fresh eggs packed by the tray for households, kiosks, and small businesses.',
                'unit': 'tray',
                'base_price': 450,
                'availability_status': Product.AVAILABLE,
                'is_active': True,
            },
        )
        self.stdout.write(self.style.SUCCESS('Puodho seed data is ready.'))
