# Generated by Django 4.2.15 on 2025-04-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0058_rename_telegramlink_coursetelegramlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetelegramlink',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='Used'),
        ),
    ]
