# Generated by Django 5.0.4 on 2024-04-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0002_user_is_futsal_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
