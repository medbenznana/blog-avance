# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-11-26 22:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_feed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feed',
        ),
    ]
