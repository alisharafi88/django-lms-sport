# Generated by Django 4.2.15 on 2024-10-15 16:09

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_remove_instructorwidjet_instructor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='img',
            field=models.ImageField(default=1, upload_to='courses/%Y/%m/%d', verbose_name='main img'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='description'),
        ),
    ]
