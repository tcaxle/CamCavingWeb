# Generated by Django 2.2 on 2020-03-22 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0019_auto_20200322_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='is_freshers_trip',
            field=models.BooleanField(default=False),
        ),
    ]
