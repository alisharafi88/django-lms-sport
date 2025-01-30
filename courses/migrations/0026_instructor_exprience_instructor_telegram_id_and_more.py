# Generated by Django 4.2.15 on 2024-09-08 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_delete_courseoptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='exprience',
            field=models.PositiveIntegerField(default=1, help_text='How many years of experience do you have?!', verbose_name='exprience'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='telegram_id',
            field=models.CharField(default=1, help_text='Your telegram id for showing in your profile!', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='youtube_id',
            field=models.CharField(default=1, help_text='Your youtube id for showing in your profile!', max_length=50),
            preserve_default=False,
        ),
    ]
