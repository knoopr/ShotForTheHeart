# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-30 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShotForTheHeart', '0009_auto_20160730_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_started',
            field=models.BooleanField(default=True),
        ),
    ]