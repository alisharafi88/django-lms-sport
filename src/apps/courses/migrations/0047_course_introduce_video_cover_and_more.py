# Generated by Django 4.2.15 on 2025-02-21 12:38

import apps.courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0046_alter_course_age_range_alter_package_age_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='introduce_video_cover',
            field=models.ImageField(blank=True, help_text='Cover of introduce video', null=True, upload_to=apps.courses.models.upload_introduce_video_cover_path, verbose_name='Cover'),
        ),
        migrations.AddField(
            model_name='package',
            name='introduce_video_cover',
            field=models.ImageField(blank=True, help_text='Cover of introduce video', null=True, upload_to=apps.courses.models.upload_introduce_video_cover_path, verbose_name='Cover'),
        ),
    ]
