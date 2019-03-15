# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-13 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventually', '0009_merge_20190313_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='fb_link',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]