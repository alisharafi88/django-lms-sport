# Generated by Django 4.2.15 on 2025-02-10 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0036_remove_coursecomments_parent_coursecomments_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomments',
            name='rate',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Rate'),
        ),
    ]
