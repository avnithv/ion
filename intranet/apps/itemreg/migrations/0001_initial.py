# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 01:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatorRegistration',
            fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('calc_serial', models.CharField(max_length=10)),
                    ('calc_id', models.CharField(max_length=14)),
                    ('calc_type', models.CharField(
                        choices=[('ti83', 'TI-83'),
                                 ('ti83p', 'TI-83+'),
                                 ('ti84p', 'TI-84+'),
                                 ('ti84pse', 'TI-84+ Silver Edition'),
                                 ('ti84pcse', 'TI-84+ C Silver Edition'),
                                 ('ti84pce', 'TI-84+ CE'),
                                 ('ti89', 'TI-89'),
                                 ('nspirecx', 'TI-Nspire CX'),
                                 ('nspirecas', 'TI-Nspire CAS'),
                                 ('otherti', 'Other TI'),
                                 ('other', 'Other')],
                        max_length=10)),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ],),
        migrations.CreateModel(
            name='ComputerRegistration',
            fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('manufacturer', models.CharField(
                        choices=[('acer', 'Acer'),
                                 ('apple', 'Apple'),
                                 ('asus', 'Asus'),
                                 ('dell', 'Dell'),
                                 ('hp', 'HP'),
                                 ('lenovo', 'Lenovo'),
                                 ('toshiba', 'Toshiba'),
                                 ('ibm', 'IBM'),
                                 ('compaq', 'Compaq'),
                                 ('fujitsu', 'Fujitsu'),
                                 ('vizio', 'Vizio'),
                                 ('other', 'Other')],
                        max_length=15)),
                    ('model', models.CharField(max_length=100)),
                    ('serial', models.CharField(max_length=20)),
                    ('description', models.CharField(max_length=1000)),
                    ('screen_size', models.PositiveIntegerField()),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ],),
        migrations.CreateModel(
            name='FoundItem',
            fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('title', models.CharField(max_length=100)),
                    ('description', models.CharField(max_length=1000)),
                    ('found', models.DateField()),
                    ('added', models.DateTimeField(auto_now_add=True)),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ],),
        migrations.CreateModel(
            name='LostItem',
            fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('title', models.CharField(max_length=100)),
                    ('description', models.CharField(max_length=1000)),
                    ('last_seen', models.DateField()),
                    ('added', models.DateTimeField(auto_now_add=True)),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ],),
        migrations.CreateModel(
            name='PhoneRegistration',
            fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('manufacturer', models.CharField(
                        choices=[('samsung', 'Samsung'),
                                 ('apple', 'Apple'),
                                 ('motorola', 'Motorola'),
                                 ('huawei', 'Huawei'),
                                 ('lg', 'LG'),
                                 ('xiaomi', 'Xiaomi'),
                                 ('zte', 'ZTE'),
                                 ('nokia', 'Nokia'),
                                 ('other', 'Other')],
                        max_length=15)),
                    ('model', models.CharField(max_length=100)),
                    ('serial', models.CharField(max_length=20)),
                    ('description', models.CharField(max_length=1000)),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ],), ]
