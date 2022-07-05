# Generated by Django 2.2 on 2020-03-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0021_trip_is_missing_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AlterField(
            model_name='album',
            name='directory',
            field=models.CharField(max_length=512, unique=True),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]