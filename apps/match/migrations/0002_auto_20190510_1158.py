# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-10 09:58
from __future__ import unicode_literals

from django.db import migrations
import match.models.generic


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotics1',
            name='sections',
            field=match.models.generic.ConstrainedCountField(default=0, max_value=8, min_value=0, verbose_name='sections parcourues'),
        ),
        migrations.AlterField(
            model_name='robotics2',
            name='sections',
            field=match.models.generic.ConstrainedCountField(default=0, max_value=8, min_value=0, verbose_name='sections parcourues'),
        ),
        migrations.AlterField(
            model_name='robotics3',
            name='captured_objects',
            field=match.models.generic.ConstrainedCountField(default=0, max_value=2, min_value=0, verbose_name='objets récupérés'),
        ),
        migrations.AlterField(
            model_name='robotics3',
            name='deposited_objects',
            field=match.models.generic.ConstrainedCountField(default=0, max_value=2, min_value=0, verbose_name='objets déposés'),
        ),
    ]
