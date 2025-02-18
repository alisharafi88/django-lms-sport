# Generated by Django 4.2.15 on 2025-02-17 23:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0041_alter_courseseason_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursevideo',
            options={'ordering': ('created_at',), 'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
        migrations.RemoveField(
            model_name='coursevideo',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursevideo',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='coursevideo',
            name='video',
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='ایجاد شده در'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='season',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='courses.courseseason', verbose_name='Season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='به\u200cروزرسانی شده در'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='status',
            field=models.CharField(choices=[('f', 'رایگان'), ('m', 'پولی')], default='m', help_text='Show that this video is free or not.', max_length=1, verbose_name='وضعیت'),
        ),
        migrations.AddIndex(
            model_name='coursevideo',
            index=models.Index(fields=['season'], name='courses_video_season_idx'),
        ),
        migrations.AddIndex(
            model_name='coursevideo',
            index=models.Index(fields=['created_at'], name='courses_video_created_at_idx'),
        ),
    ]
