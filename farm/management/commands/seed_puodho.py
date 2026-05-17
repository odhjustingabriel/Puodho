from django.core.management.base import BaseCommand
from farm.models import Category, Product, ProductOption


class Command(BaseCommand):
    help = 'Seed Puodho with starter farm produce across poultry, eggs, livestock, and milk.'

    def handle(self, *args, **options):
        categories = {
            'Poultry': 'Fresh broiler chickens and poultry produce.',
            'Eggs': 'Farm fresh eggs sold by the tray.',
            'Cattle': 'Dairy, beef, and hardy dual-purpose cattle available by age and breed.',
            'Goats': 'Meat and dairy goats suited for local homes, farms, and breeding needs.',
            'Sheep': 'Hardy meat, wool, and dual-purpose sheep breeds commonly reared in Kenya.',
            'Milk Products': 'Cow, goat, and specialty milk requests handled by availability.',
        }
        category_map = {}
        for name, description in categories.items():
            category, _ = Category.objects.get_or_create(name=name, defaults={'description': description})
            if category.description != description:
                category.description = description
                category.save(update_fields=['description'])
            category_map[name] = category

        broiler, _ = Product.objects.update_or_create(
            slug='broiler-chicken',
            defaults={
                'category': category_map['Poultry'],
                'name': 'Broiler Chicken',
                'description': 'Healthy farm-raised broiler chickens available alive or prepared for your kitchen.',
                'unit': 'whole chicken',
                'base_price': 650,
                'availability_status': Product.AVAILABLE,
                'is_active': True,
            },
        )
        self._sync_options(broiler, [
            ('Alive', 650, 'Live broiler chicken.'),
            ('Prepared', 750, 'Slaughtered and skinned broiler chicken.'),
        ])

        Product.objects.update_or_create(
            slug='eggs',
            defaults={
                'category': category_map['Eggs'],
                'name': 'Eggs',
                'description': 'Fresh eggs packed by the tray for households, kiosks, and small businesses.',
                'unit': 'tray',
                'base_price': 450,
                'availability_status': Product.AVAILABLE,
                'is_active': True,
            },
        )

        cattle, _ = Product.objects.update_or_create(
            slug='cattle',
            defaults={
                'category': category_map['Cattle'],
                'name': 'Cows / Cattle',
                'description': 'Dairy, beef, and hardy cattle requests by breed and age. Prices vary by stage, health, and availability.',
                'unit': 'animal',
                'base_price': 25000,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(cattle, [
            ('Friesian / Holstein Friesian calf', 45000, 'Dairy breed. Suggested sale age: calves 3–6 months.'),
            ('Friesian / Holstein heifer or cow', 140000, 'Dairy heifers 10–15 months, in-calf or lactating cows 18+ months.'),
            ('Ayrshire heifer or in-calf cow', 100000, 'Dairy breed. Usually sold as heifers or in-calf cows from 12+ months.'),
            ('Sahiwal calf / heifer / cow', 25000, 'Hardy dual-purpose dairy/beef breed. Calves 6–12 months, heifers 12–24 months, mature cows 24+ months.'),
            ('Boran young stock or mature cattle', 100000, 'Hardy beef cattle. Young stock 8–18 months, mature cattle 24+ months.'),
        ])

        goats, _ = Product.objects.update_or_create(
            slug='goats',
            defaults={
                'category': category_map['Goats'],
                'name': 'Goats',
                'description': 'Hardy meat and dairy goats available by breed, age, and farm availability.',
                'unit': 'goat',
                'base_price': 12000,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(goats, [
            ('Galla goat', 12000, 'Meat and hardy dual-purpose goat. Young stock 6–12 months, breeding stock 12+ months.'),
            ('Boer goat', 30000, 'Meat goat. Usually sold from 6–12 months for meat or breeding stock.'),
            ('Saanen dairy goat', 15000, 'Dairy goat. Usually sold at 8–18 months or as a lactating doe.'),
            ('Toggenburg / Alpine dairy goat', 25000, 'Dairy goat. Usually sold at 8–18 months or as a lactating doe.'),
        ])

        sheep, _ = Product.objects.update_or_create(
            slug='sheep',
            defaults={
                'category': category_map['Sheep'],
                'name': 'Sheep',
                'description': 'Meat, wool, and hardy sheep breeds available by size, age, and suitability.',
                'unit': 'sheep',
                'base_price': 5000,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(sheep, [
            ('Dorper sheep', 15000, 'Meat breed. Market lambs often 5–9 months; breeding stock 12+ months.'),
            ('Red Maasai sheep', 5000, 'Hardy meat breed. Meat stock 6–12 months; breeding stock 14+ months.'),
            ('Blackhead Persian sheep', 8000, 'Hardy meat breed, commonly sold from 6–12 months depending on size.'),
            ('Merino sheep', 5000, 'Wool or dual-purpose breed. Young stock 6–12 months; breeding stock later.'),
        ])

        cow_milk, _ = Product.objects.update_or_create(
            slug='cow-milk',
            defaults={
                'category': category_map['Milk Products'],
                'name': 'Cow Milk',
                'description': 'Fresh cow milk from dairy cattle such as Friesian, Ayrshire, Sahiwal, and crosses.',
                'unit': 'litre',
                'base_price': 60,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(cow_milk, [
            ('Per litre', 60, 'Starter website price within the Ksh 50–80 per litre range.'),
            ('Bulk cow milk order', 0, 'Custom quantity. Quote on request after availability confirmation.'),
        ])

        goat_milk, _ = Product.objects.update_or_create(
            slug='goat-milk',
            defaults={
                'category': category_map['Milk Products'],
                'name': 'Goat Milk',
                'description': 'Goat milk from dairy breeds such as Saanen, Toggenburg, Alpine, and Galla where available.',
                'unit': 'litre',
                'base_price': 200,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(goat_milk, [
            ('Per litre', 200, 'Starter website price within the Ksh 150–250 per litre range.'),
            ('Bulk goat milk order', 0, 'Custom quantity. Quote on request after availability confirmation.'),
        ])

        sheep_milk, _ = Product.objects.update_or_create(
            slug='sheep-milk',
            defaults={
                'category': category_map['Milk Products'],
                'name': 'Sheep Milk',
                'description': 'Specialty sheep milk requests are handled only when production and demand make supply practical.',
                'unit': 'litre',
                'base_price': 0,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(sheep_milk, [
            ('Available on inquiry', 0, 'No fixed website price yet because sheep milk is niche locally.'),
        ])

        bulk_milk, _ = Product.objects.update_or_create(
            slug='bulk-milk-order',
            defaults={
                'category': category_map['Milk Products'],
                'name': 'Bulk Milk Order',
                'description': 'Custom cow or goat milk quantities for households, shops, or institutions. Quote depends on volume and availability.',
                'unit': 'custom quantity',
                'base_price': 0,
                'availability_status': Product.LIMITED,
                'is_active': True,
            },
        )
        self._sync_options(bulk_milk, [
            ('Quote on request', 0, 'Puodho confirms litres, collection/delivery plan, and final price before fulfillment.'),
        ])

        self.stdout.write(self.style.SUCCESS('Puodho seed data is ready with poultry, eggs, livestock, and milk products.'))

    def _sync_options(self, product, options):
        for name, price, description in options:
            ProductOption.objects.update_or_create(
                product=product,
                name=name,
                defaults={'price': price, 'description': description, 'is_active': True},
            )
