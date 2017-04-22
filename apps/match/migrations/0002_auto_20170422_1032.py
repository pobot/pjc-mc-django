# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-22 08:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_squashed_0009_auto_20170417_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotics1',
            name='variants',
            field=models.PositiveSmallIntegerField(default=0, validators=django.core.validators.MaxValueValidator(2), verbose_name='variantes'),
        ),
    ]