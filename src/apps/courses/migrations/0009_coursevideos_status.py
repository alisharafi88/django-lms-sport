# Generated by Django 4.2.15 on 2024-08-26 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_coursevideos'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursevideos',
            name='status',
            field=models.CharField(choices=[('m', 'Monetary'), ('f', 'Free')], default=1, help_text='Show that this video is free or not.', max_length=1, verbose_name='status'),
            preserve_default=False,
        ),
    ]
