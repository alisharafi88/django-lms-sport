# Generated by Django 4.2.15 on 2025-03-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0052_alter_course_date_created_alter_course_date_modified_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='course',
            name='course_active_discounts_idx',
        ),
        migrations.RemoveIndex(
            model_name='package',
            name='package_active_discounts_idx',
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['price', 'status'], name='course_price_status_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['status'], name='course_status_covering_idx'),
        ),
        migrations.AddIndex(
            model_name='package',
            index=models.Index(fields=['price', 'status'], name='package_price_status_idx'),
        ),
        migrations.AddIndex(
            model_name='package',
            index=models.Index(fields=['status'], name='package_status_covering_idx'),
        ),
    ]
