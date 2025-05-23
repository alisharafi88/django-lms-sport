# Generated by Django 4.2.15 on 2025-03-23 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0007_alter_contactinfo_adress_alter_contactinfo_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'verbose_name': 'Contact Information', 'verbose_name_plural': 'Contact Information'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.RemoveField(
            model_name='contactinfo',
            name='adress',
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='address',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='instagram_id',
            field=models.CharField(blank=True, help_text='Enter your Instagram ID.', max_length=50, null=True, verbose_name='instagram id'),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='telegram_id',
            field=models.CharField(blank=True, help_text='Enter your Telegram ID.', max_length=50, null=True, verbose_name='telegram id'),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='youtube_id',
            field=models.CharField(blank=True, help_text='Enter your YouTube ID.', max_length=50, null=True, verbose_name='youtube id'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='is_primary',
            field=models.BooleanField(help_text='you can only have 1 primary contact', verbose_name='Is primary'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='phonenumber',
            field=models.CharField(max_length=11, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_sent',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date sent'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
