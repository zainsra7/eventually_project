# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-08 15:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventually', '0003_auto_20190208_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
