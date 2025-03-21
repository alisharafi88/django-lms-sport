# Generated by Django 4.2.15 on 2024-08-25 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='VipPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('age_range', models.CharField(help_text='Age range for users.', max_length=50, verbose_name='age range')),
                ('duration', models.CharField(help_text='How long it takes to complete this course?.', max_length=10, verbose_name='duration')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='Discount amount for course.', max_digits=5, verbose_name='discount amount')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created at')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified at')),
                ('status', models.BooleanField(default=True, help_text='Show that this course is active or no.', verbose_name='status')),
                ('certificate_status', models.BooleanField(help_text='Show that this course have certificate or no.', verbose_name='certificate')),
                ('courses', models.ManyToManyField(related_name='vip_packages', to='courses.course', verbose_name='Courses')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
