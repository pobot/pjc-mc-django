# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20171105_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='email',
            field=models.EmailField(blank=True, max_length=150, verbose_name='email'),
        ),
    ]
