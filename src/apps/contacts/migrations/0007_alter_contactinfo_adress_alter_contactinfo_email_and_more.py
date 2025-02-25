# Generated by Django 4.2.15 on 2025-02-08 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0006_alter_contactinfo_is_primary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='adress',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=255, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='آدرس ایمیل'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='is_primary',
            field=models.BooleanField(help_text='شما فقط می\u200cتوانید یک تماس اصلی داشته باشید', verbose_name='آیا اصلی است'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='phonenumber',
            field=models.CharField(max_length=11, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_sent',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='پیام'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
