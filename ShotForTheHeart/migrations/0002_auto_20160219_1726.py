# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShotForTheHeart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to=b'./'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='study_year',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
