# Generated by Django 2.2.4 on 2019-08-27 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0020_auto_20190827_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='open',
        ),
    ]
