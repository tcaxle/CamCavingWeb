# Generated by Django 2.2 on 2020-03-22 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0020_trip_is_freshers_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='is_missing_info',
            field=models.BooleanField(default=False),
        ),
    ]
