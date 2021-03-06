# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 10:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nom')),
                ('city', models.CharField(max_length=50, verbose_name='ville')),
                ('zip_code', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$', message='Code postal invalide')], verbose_name='code postal')),
            ],
            options={
                'verbose_name': 'établissement scolaire',
                'verbose_name_plural': 'établissements scolaires',
                'ordering': ['zip_code', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False, verbose_name='numéro')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='nom')),
                ('grade_code', models.SmallIntegerField(choices=[(1, 'PostBAC'), (2, 'Terminale'), (3, 'Première'), (4, 'Seconde'), (5, 'Troisième'), (6, 'Quatrième'), (7, 'Cinquième'), (8, 'Sixième'), (9, 'CM2'), (10, 'CM1')], default=8, verbose_name='niveau scolaire')),
                ('category_code', models.SmallIntegerField(choices=[(1, 'Mindstorms'), (2, 'Arduino'), (3, 'RaspberryPi')], default=1, verbose_name='catégorie')),
                ('present', models.BooleanField(default=False, verbose_name='présente')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='teams.School', verbose_name='établissement scolaire')),
            ],
            options={
                'verbose_name': 'équipe',
                'ordering': ['num'],
            },
        ),
    ]
