# Generated by Django 2.2.4 on 2019-08-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0005_account_account_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_key',
            field=models.CharField(default='d63df9a9eccb4b729487ebf26be2af77', editable=False, max_length=32),
        ),
    ]
