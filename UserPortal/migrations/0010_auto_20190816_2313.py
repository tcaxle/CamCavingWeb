# Generated by Django 2.2.3 on 2019-08-16 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPortal', '0009_auto_20190816_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mailing_list',
            field=models.BooleanField(default=False, verbose_name='Subscribe to Mailing List?'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.CharField(default='61f49f8600754e838f6697bb7d844cdb', max_length=32),
        ),
    ]
