# Generated by Django 2.2 on 2020-03-19 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0011_auto_20200319_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(default='', max_length=100),
        ),
    ]
