# Generated by Django 4.2.15 on 2024-08-31 22:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0012_alter_coursevideo_video_coursemembership'),
    ]

    operations = [
        migrations.CreateModel(
            name='VipPackageMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vips', to=settings.AUTH_USER_MODEL, verbose_name='Vip package membership')),
                ('vip_package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='courses.vippackage', verbose_name='Vip package')),
            ],
            options={
                'unique_together': {('user', 'vip_package')},
            },
        ),
    ]
