# Generated by Django 4.2.15 on 2025-04-10 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='coupon',
            new_name='coupon_code',
        ),
    ]
