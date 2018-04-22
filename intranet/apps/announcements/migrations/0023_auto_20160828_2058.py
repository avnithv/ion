# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 00:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [('announcements', '0022_auto_20151118_1037')]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='announcementrequest',
            name='posted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posted_by',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='announcementrequest',
            name='rejected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rejected_by',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='announcementrequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
