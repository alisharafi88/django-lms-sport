# Generated by Django 4.2.15 on 2025-03-26 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_ticket_options_alter_ticketreply_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create Date'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
    ]
