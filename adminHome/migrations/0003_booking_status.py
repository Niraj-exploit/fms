# Generated by Django 5.0.1 on 2024-01-23 13:39

import adminHome.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminHome', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[(adminHome.models.BookingStatus['PENDING'], 'PENDING'), (adminHome.models.BookingStatus['CONFIRMED'], 'CONFIRMED'), (adminHome.models.BookingStatus['CANCELLED'], 'CANCELLED')], default=adminHome.models.BookingStatus['PENDING'], max_length=10),
        ),
    ]
