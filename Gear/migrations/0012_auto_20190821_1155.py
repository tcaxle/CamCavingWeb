# Generated by Django 2.2.4 on 2019-08-21 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gear', '0011_auto_20190821_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hirerope',
            options={'permissions': [('hire_rope_self', 'Can hire rope on their own behalf'), ('hire_rope_other', 'Can hire rope on behalf of others')]},
        ),
    ]
