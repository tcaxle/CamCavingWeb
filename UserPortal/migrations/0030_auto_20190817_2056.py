# Generated by Django 2.2.4 on 2019-08-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPortal', '0029_auto_20190817_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='meets_secretary',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.CharField(default='3df3e0883f514658a8483c875184a473', max_length=32),
        ),
    ]
