# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-03-14 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_auto_20190519_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotics2',
            name='object_retrieved',
            field=models.BooleanField(default=False, verbose_name='objet récupéré ?'),
        ),
    ]
