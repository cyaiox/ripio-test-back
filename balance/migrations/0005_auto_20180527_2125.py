# Generated by Django 2.0.5 on 2018-05-27 21:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0004_auto_20180513_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfers',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
