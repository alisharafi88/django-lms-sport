# Generated by Django 4.2.15 on 2025-04-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_counter_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counter',
            name='reviews',
        ),
        migrations.AddField(
            model_name='counter',
            name='comments',
            field=models.IntegerField(default=5, verbose_name='Comments'),
        ),
    ]
