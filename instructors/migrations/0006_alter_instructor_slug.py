# Generated by Django 4.2.15 on 2024-09-09 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0005_instructor_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, verbose_name='slug'),
        ),
    ]
