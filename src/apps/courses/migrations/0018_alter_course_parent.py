# Generated by Django 4.2.15 on 2024-09-04 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_vippackagemembership_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='parent',
            field=models.ManyToManyField(blank=True, related_name='packages', to='courses.course', verbose_name='Courses'),
        ),
    ]
