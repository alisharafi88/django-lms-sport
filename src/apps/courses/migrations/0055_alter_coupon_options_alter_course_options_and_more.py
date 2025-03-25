# Generated by Django 4.2.15 on 2025-03-25 23:01

import apps.courses.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0016_alter_instructor_options_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0054_alter_coursemembership_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Coupon', 'verbose_name_plural': 'Coupons'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterModelOptions(
            name='coursecomments',
            options={'ordering': ('-date_created',), 'verbose_name': "course's comment", 'verbose_name_plural': "course's comments"},
        ),
        migrations.AlterModelOptions(
            name='coursemembership',
            options={'verbose_name': 'Course Membership', 'verbose_name_plural': 'Course Memberships'},
        ),
        migrations.AlterModelOptions(
            name='courseseason',
            options={'ordering': ('created_at',), 'verbose_name': 'Season', 'verbose_name_plural': 'Seasons'},
        ),
        migrations.AlterModelOptions(
            name='coursevideo',
            options={'ordering': ('created_at',), 'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
        migrations.AlterModelOptions(
            name='package',
            options={'verbose_name': 'Package', 'verbose_name_plural': 'Packages'},
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=50, unique=True, verbose_name='Code of coupon'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='date_valid_from',
            field=models.DateField(verbose_name='Date valid from'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='date_valid_to',
            field=models.DateField(verbose_name='Date valid to'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Discount amount'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='max_usage_per_user',
            field=models.IntegerField(default=1, help_text='Number of people who can use.', verbose_name='Max number of usage'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='course',
            name='age_range',
            field=models.CharField(help_text='Age range for users.', max_length=12, verbose_name='Age range'),
        ),
        migrations.AlterField(
            model_name='course',
            name='analysis_room_status',
            field=models.BooleanField(default=False, verbose_name='Analysis room'),
        ),
        migrations.AlterField(
            model_name='course',
            name='certificate_status',
            field=models.BooleanField(default=False, help_text='Show that this course have certificate or no.', verbose_name='Certificate'),
        ),
        migrations.AlterField(
            model_name='course',
            name='coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='instructors.instructor', verbose_name='Coach'),
        ),
        migrations.AlterField(
            model_name='course',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date created at'),
        ),
        migrations.AlterField(
            model_name='course',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date modified at'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Discount amount for this product.', max_digits=5, verbose_name='Discount amount'),
        ),
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.CharField(help_text='How long it takes to complete this course?.', max_length=10, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='course',
            name='extra_movments_status',
            field=models.BooleanField(default=False, verbose_name='Extra movments'),
        ),
        migrations.AlterField(
            model_name='course',
            name='img',
            field=models.ImageField(upload_to=apps.courses.models.upload_introduce_image_path, verbose_name='Main Image'),
        ),
        migrations.AlterField(
            model_name='course',
            name='injury_prevention_status',
            field=models.BooleanField(default=False, verbose_name='Injury prevention'),
        ),
        migrations.AlterField(
            model_name='course',
            name='introduce_video_cover',
            field=models.ImageField(blank=True, help_text='Cover of introduce video', null=True, upload_to=apps.courses.models.upload_introduce_video_cover_path, verbose_name="Video's Cover"),
        ),
        migrations.AlterField(
            model_name='course',
            name='introduce_video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Introduce Video URL'),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.BooleanField(db_index=True, default=True, help_text='Show that this product is active or not.', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='rate',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='status',
            field=models.BooleanField(default=True, help_text='If the comment is not appropriate, set it to false.', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='text',
            field=models.TextField(verbose_name='Text of the comment'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_comments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='coursemembership',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('course', 'package')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content Type'),
        ),
        migrations.AlterField(
            model_name='coursemembership',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='coursemembership',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified Date'),
        ),
        migrations.AlterField(
            model_name='coursemembership',
            name='object_id',
            field=models.PositiveIntegerField(verbose_name='Object ID'),
        ),
        migrations.AlterField(
            model_name='coursemembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL, verbose_name='User Membership'),
        ),
        migrations.AlterField(
            model_name='courseseason',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='courses.course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='courseseason',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creat Date'),
        ),
        migrations.AlterField(
            model_name='courseseason',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='courseseason',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='courses.courseseason', verbose_name='Season'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='status',
            field=models.CharField(choices=[('f', 'Free'), ('m', 'Monetary')], default='m', help_text='Show that this video is free or not.', max_length=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='coursevideo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='package',
            name='age_range',
            field=models.CharField(help_text='Age range for users.', max_length=12, verbose_name='Age range'),
        ),
        migrations.AlterField(
            model_name='package',
            name='analysis_room_status',
            field=models.BooleanField(default=False, verbose_name='Analysis room'),
        ),
        migrations.AlterField(
            model_name='package',
            name='certificate_status',
            field=models.BooleanField(default=False, help_text='Show that this course have certificate or no.', verbose_name='Certificate'),
        ),
        migrations.AlterField(
            model_name='package',
            name='courses',
            field=models.ManyToManyField(to='courses.course', verbose_name='Courses in this package'),
        ),
        migrations.AlterField(
            model_name='package',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date created at'),
        ),
        migrations.AlterField(
            model_name='package',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date modified at'),
        ),
        migrations.AlterField(
            model_name='package',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='package',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Discount amount for this product.', max_digits=5, verbose_name='Discount amount'),
        ),
        migrations.AlterField(
            model_name='package',
            name='duration',
            field=models.CharField(help_text='How long it takes to complete this course?.', max_length=10, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='package',
            name='extra_movments_status',
            field=models.BooleanField(default=False, verbose_name='Extra movments'),
        ),
        migrations.AlterField(
            model_name='package',
            name='img',
            field=models.ImageField(upload_to=apps.courses.models.upload_introduce_image_path, verbose_name='Main Image'),
        ),
        migrations.AlterField(
            model_name='package',
            name='injury_prevention_status',
            field=models.BooleanField(default=False, verbose_name='Injury prevention'),
        ),
        migrations.AlterField(
            model_name='package',
            name='introduce_video_cover',
            field=models.ImageField(blank=True, help_text='Cover of introduce video', null=True, upload_to=apps.courses.models.upload_introduce_video_cover_path, verbose_name="Video's Cover"),
        ),
        migrations.AlterField(
            model_name='package',
            name='introduce_video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Introduce Video URL'),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='package',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.BooleanField(db_index=True, default=True, help_text='Show that this product is active or not.', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='package',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Title'),
        ),
    ]
