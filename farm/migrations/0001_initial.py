# Generated manually for Puodho farm app
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name_plural': 'categories', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_reference', models.CharField(blank=True, max_length=30, unique=True)),
                ('customer_name', models.CharField(max_length=160)),
                ('phone', models.CharField(max_length=40)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('location', models.CharField(max_length=220)),
                ('delivery_method', models.CharField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], max_length=20)),
                ('preferred_date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready_for_pickup', 'Ready for Pickup'), ('out_for_delivery', 'Out for Delivery'), ('completed', 'Completed'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=30)),
                ('admin_note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True)),
                ('description', models.TextField()),
                ('unit', models.CharField(max_length=80)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.URLField(blank=True)),
                ('availability_status', models.CharField(choices=[('available', 'Available'), ('limited', 'Limited'), ('unavailable', 'Unavailable')], default='available', max_length=20)),
                ('stock_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='farm.category')),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='farm.product')),
            ],
            options={'ordering': ['product__name', 'price'], 'unique_together': {('product', 'name')}},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('line_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='farm.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farm.product')),
                ('product_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='farm.productoption')),
            ],
        ),
    ]
