# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-25 21:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20161212_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='app',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='free_resp',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='is_writing',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='short_resp',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='std',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='std_other',
        ),
    ]
