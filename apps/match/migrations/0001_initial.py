# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-24 14:54
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import match.models.generic


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0013_auto_20190217_0014'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Robotics1',
            fields=[
                ('team', models.OneToOneField(error_messages={'unique': 'Données déjà saisies pour cette équipe.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='heure de passage')),
                ('used_time', match.models.generic.MatchDurationField(default=datetime.timedelta(0, 150), validators=[django.core.validators.MaxValueValidator(datetime.timedelta(0, 150))], verbose_name='temps utilisé')),
                ('sections', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=8)], verbose_name='sections parcourues')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='arbitre')),
            ],
            options={
                'verbose_name': 'résultat épreuve 1',
                'verbose_name_plural': 'résultats épreuve 1',
            },
        ),
        migrations.CreateModel(
            name='Robotics2',
            fields=[
                ('team', models.OneToOneField(error_messages={'unique': 'Données déjà saisies pour cette équipe.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='heure de passage')),
                ('used_time', match.models.generic.MatchDurationField(default=datetime.timedelta(0, 150), validators=[django.core.validators.MaxValueValidator(datetime.timedelta(0, 150))], verbose_name='temps utilisé')),
                ('sections', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=8)], verbose_name='sections parcourues')),
                ('object_retrieved', models.BooleanField(default=0, verbose_name='objet récupéré')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='arbitre')),
            ],
            options={
                'verbose_name': 'résultat épreuve 2',
                'verbose_name_plural': 'résultats épreuve 2',
            },
        ),
        migrations.CreateModel(
            name='Robotics3',
            fields=[
                ('team', models.OneToOneField(error_messages={'unique': 'Données déjà saisies pour cette équipe.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='heure de passage')),
                ('used_time', match.models.generic.MatchDurationField(default=datetime.timedelta(0, 150), validators=[django.core.validators.MaxValueValidator(datetime.timedelta(0, 150))], verbose_name='temps utilisé')),
                ('captured_objects', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=2)], verbose_name='objets récupérés')),
                ('deposited_objects', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=2)], verbose_name='objets déposés')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='arbitre')),
            ],
            options={
                'verbose_name': 'résultat épreuve 3',
                'verbose_name_plural': 'résultats épreuve 3',
            },
        ),
    ]
