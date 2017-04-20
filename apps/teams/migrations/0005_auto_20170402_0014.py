# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_team_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='grade',
        ),
        migrations.AddField(
            model_name='team',
            name='grade_code',
            field=models.SmallIntegerField(choices=[(1, 'post_bac'), (2, 'terminale'), (3, 'premiere'), (4, 'seconde'), (5, 'troisieme'), (6, 'quatrieme'), (7, 'cinquieme'), (8, 'sixieme'), (9, 'cm2'), (10, 'cm1')], default=8, verbose_name='niveau scolaire'),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=50, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='team',
            name='category',
            field=models.SmallIntegerField(choices=[(1, 'Mindstorms'), (2, 'Arduino'), (3, 'PiStorms')], default=1, verbose_name='catégorie'),
        ),
    ]
