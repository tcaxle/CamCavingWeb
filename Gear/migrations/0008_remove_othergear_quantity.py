# Generated by Django 2.2.3 on 2019-08-21 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gear', '0007_hireoversuit_hireundersuit_oversuit_undersuit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='othergear',
            name='quantity',
        ),
    ]
