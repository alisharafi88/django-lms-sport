# Generated by Django 4.2.15 on 2024-09-09 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0003_instructor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='status',
            field=models.BooleanField(default=True, verbose_name='status'),
        ),
    ]
