# Generated by Django 4.2.15 on 2025-04-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='reviews',
            field=models.IntegerField(default=5, verbose_name='Reviews'),
        ),
    ]
