# Generated by Django 4.2.15 on 2025-04-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
