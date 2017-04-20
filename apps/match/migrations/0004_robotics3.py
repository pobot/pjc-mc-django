# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 23:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20170220_0013'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0003_auto_20170220_2345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robotics3',
            fields=[
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='heure de passage')),
                ('trips', models.PositiveSmallIntegerField(default=0, verbose_name='trajets')),
                ('variants', models.PositiveSmallIntegerField(default=0, verbose_name='variantes')),
                ('moved_obstacles', models.PositiveSmallIntegerField(default=0, verbose_name='obstacles déplacés')),
                ('referee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='arbitre')),
            ],
            options={
                'verbose_name': 'score robotique 3',
                'verbose_name_plural': 'scores robotique 3',
            },
        ),
    ]
