# Generated by Django 4.2.16 on 2024-12-01 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_customuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
    ]