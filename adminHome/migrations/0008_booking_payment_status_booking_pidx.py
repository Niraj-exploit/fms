# Generated by Django 5.0.4 on 2024-04-06 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminHome', '0007_booking_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='pidx',
            field=models.CharField(max_length=20, null=True),
        ),
    ]