# Generated by Django 4.2.15 on 2025-02-21 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0044_package_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='age_range',
            field=models.CharField(help_text='محدوده سنی برای کاربران.', max_length=10, verbose_name='Age range'),
        ),
        migrations.AlterField(
            model_name='package',
            name='age_range',
            field=models.CharField(help_text='محدوده سنی برای کاربران.', max_length=10, verbose_name='Age range'),
        ),
    ]
