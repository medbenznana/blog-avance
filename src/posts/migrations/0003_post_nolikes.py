# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-11-19 13:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nolikes',
            field=models.ManyToManyField(blank=True, related_name='post_nolikes', to=settings.AUTH_USER_MODEL),
        ),
    ]