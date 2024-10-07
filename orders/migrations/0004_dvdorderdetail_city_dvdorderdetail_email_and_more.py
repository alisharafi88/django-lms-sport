# Generated by Django 4.2.15 on 2024-10-05 19:16

from django.db import migrations, models
import orders.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_dvdorderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='dvdorderdetail',
            name='city',
            field=models.CharField(default='th', max_length=15, verbose_name='city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dvdorderdetail',
            name='email',
            field=models.EmailField(default='mm@gmail.com', max_length=254, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dvdorderdetail',
            name='first_name',
            field=models.CharField(default='a', max_length=20, verbose_name='first name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dvdorderdetail',
            name='last_name',
            field=models.CharField(default='s', max_length=30, verbose_name='last name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dvdorderdetail',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='09334300850', max_length=128, region='IR', unique=True, validators=[orders.models.phone_number_validator_for_iran], verbose_name='phonenumber'),
            preserve_default=False,
        ),
    ]
