# Generated by Django 2.2.4 on 2019-08-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gear', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harness',
            name='uid',
            field=models.IntegerField(verbose_name='UID'),
        ),
        migrations.AlterField(
            model_name='helmet',
            name='uid',
            field=models.IntegerField(verbose_name='UID'),
        ),
        migrations.AlterField(
            model_name='othergear',
            name='in_store',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='othergear',
            name='on_loan',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='othergear',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rope',
            name='diameter',
            field=models.IntegerField(verbose_name='Diameter (mm)'),
        ),
        migrations.AlterField(
            model_name='rope',
            name='length',
            field=models.IntegerField(verbose_name='Length (m)'),
        ),
        migrations.AlterField(
            model_name='signinothergear',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='signoutothergear',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
