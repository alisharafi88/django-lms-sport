# Generated by Django 4.2.15 on 2025-02-28 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_alter_blog_options_alter_blogcomment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
