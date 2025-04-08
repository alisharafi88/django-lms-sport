# Generated by Django 4.2.15 on 2025-04-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_orderitem_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-date_created',), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.RenameIndex(
            model_name='order',
            new_name='status_zarinpal_authority_idx',
            old_name='orders_orde_status_7409f4_idx',
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['date_created'], name='date_created_idx'),
        ),
    ]
