# Generated by Django 2.2.4 on 2019-08-30 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0033_account_sort_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['sort_name'], 'permissions': [('view_own__account', 'Can view own account'), ('view_other__account', "Can view others' accounts")]},
        ),
    ]