# Generated by Django 4.2.15 on 2025-04-05 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0056_alter_coupon_discount_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_link', models.URLField(unique=True, verbose_name='Telegram Invite Link')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('date_update', models.DateTimeField(auto_now_add=True, verbose_name='Update Date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telegram_links', to='courses.course', verbose_name='Course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telegram_links', to=settings.AUTH_USER_MODEL, verbose_name='Assigned User')),
            ],
            options={
                'verbose_name': 'Telegram Link',
                'verbose_name_plural': 'Telegram Links',
            },
        ),
    ]
