# Generated by Django 4.2.15 on 2024-09-21 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='DVDOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal code')),
                ('order_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='order note')),
                ('delivery_status', models.CharField(choices=[('p', 'Pending'), ('s', 'Sent'), ('r', 'Rejected'), ('c', 'Canceled')], default='p', max_length=1, verbose_name='delivery status')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dvd_detail', to='orders.order', verbose_name='order')),
            ],
        ),
    ]
