# Generated by Django 4.2.15 on 2025-02-15 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0014_alter_instructor_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='img',
        ),
    ]
