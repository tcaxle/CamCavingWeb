# Generated by Django 2.2 on 2020-02-24 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_auto_20200115_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='parent',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.Album'),
        ),
        migrations.AlterField(
            model_name='album',
            name='directory',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]