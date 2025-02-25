# Generated by Django 4.2.15 on 2024-09-06 20:54

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150, verbose_name='question')),
                ('answer', django_ckeditor_5.fields.CKEditor5Field(verbose_name='answer')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'verbose_name': 'question and answer',
                'verbose_name_plural': 'questions and answers',
                'ordering': ('date_modified',),
            },
        ),
    ]
