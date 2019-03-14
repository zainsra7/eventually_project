# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-12 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventually', '0007_auto_20190309_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.URLField(blank=True),
        ),
    ]