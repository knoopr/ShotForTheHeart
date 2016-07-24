# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-03 16:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_email', models.CharField(max_length=127, unique=True, validators=[django.core.validators.RegexValidator(re.compile(b'[a-zA-Z0-9_\\.\\+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-\\.]+'), 'Enter a valid email.', b'ERROR')])),
                ('full_name', models.CharField(blank=True, max_length=126)),
                ('study_program', models.CharField(blank=True, max_length=50)),
                ('study_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('hangout_spot', models.CharField(blank=True, max_length=50)),
                ('profile_photo', models.ImageField(blank=True, upload_to=b'tmp')),
                ('user_eliminated', models.BooleanField(default=False)),
                ('target_id', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can login to the admin site', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text=b'Whether the user is active or not, set to false instead of deleting accounts', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
