# Generated by Django 2.2 on 2020-03-23 22:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0022_auto_20200323_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_filename', models.CharField(max_length=512)),
                ('thumb_filename', models.CharField(max_length=512)),
                ('photographer', models.CharField(blank=True, default='', max_length=100)),
                ('timestamp', models.DateTimeField(default=None, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.Album')),
            ],
        ),
    ]
