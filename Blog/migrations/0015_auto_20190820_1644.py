# Generated by Django 2.2.4 on 2019-08-20 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_auto_20190820_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='images',
            new_name='image',
        ),
    ]
