# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-30 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShotForTheHeart', '0007_auto_20160730_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='target_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
