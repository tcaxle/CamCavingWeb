# Generated by Django 2.2 on 2020-03-19 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0010_auto_20200319_0014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='posted_by',
        ),
    ]
