# Generated by Django 5.1.3 on 2024-11-28 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='password',
            field=models.CharField(default=1234, max_length=50),
            preserve_default=False,
        ),
    ]