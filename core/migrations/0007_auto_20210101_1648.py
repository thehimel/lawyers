# Generated by Django 3.1 on 2021-01-01 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_appointment_cancelled_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled_by_customer',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled_by_lawyer',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled_by_manager',
        ),
    ]