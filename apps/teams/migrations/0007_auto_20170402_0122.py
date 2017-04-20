# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 23:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20170402_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.School', verbose_name='établissement scolaire'),
        ),
    ]
