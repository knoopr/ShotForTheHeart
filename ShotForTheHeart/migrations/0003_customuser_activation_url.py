# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-14 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShotForTheHeart', '0002_auto_20160219_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_url',
            field=models.CharField(blank=True, max_length=126),
        ),
    ]
