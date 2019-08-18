# Generated by Django 2.2.4 on 2019-08-17 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPortal', '0019_auto_20190817_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('Frequent', 'Active - Frequent'), ('Infrequent', 'Active - Infrequent'), ('Expo', 'Active - Expo'), ('Inactive', 'Inactive')], default='Inactive', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.CharField(default='1a1cd7ffb7154b0099e4603532368d22', max_length=32),
        ),
    ]