# Generated by Django 2.2.4 on 2019-08-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPortal', '0007_auto_20190816_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='tape_colour1',
            new_name='tape_colour_1',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='tape_colour2',
            new_name='tape_colour_2',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='tape_colour3',
            new_name='tape_colour_3',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.CharField(default='405c8c80f07341b9867662bc2faef6d9', max_length=20),
        ),
    ]
