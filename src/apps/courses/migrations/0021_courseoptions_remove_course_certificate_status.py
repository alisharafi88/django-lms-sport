# Generated by Django 4.2.15 on 2024-09-04 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_alter_course_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='title')),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='certificate_status',
        ),
    ]
