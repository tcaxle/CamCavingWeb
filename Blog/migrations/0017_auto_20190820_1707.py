# Generated by Django 2.2.4 on 2019-08-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0016_auto_20190820_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('News', 'News'), ('Caving', 'Caving'), ('Training', 'Training'), ('Social', 'Social')], max_length=10),
        ),
    ]