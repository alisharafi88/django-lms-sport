# Generated by Django 4.2.15 on 2025-04-12 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_shippingsettings_order_dvd_shipping_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingsettings',
            options={'ordering': ('-date_updated',), 'verbose_name': 'Shipping Settings', 'verbose_name_plural': 'Shipping Settings'},
        ),
    ]
