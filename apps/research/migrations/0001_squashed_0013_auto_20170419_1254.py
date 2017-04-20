# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('research', '0001_initial'), ('research', '0002_poster'), ('research', '0003_planning'), ('research', '0004_auto_20170402_1428'), ('research', '0005_auto_20170402_1617'), ('research', '0006_auto_20170402_1617'), ('research', '0007_auto_20170402_1618'), ('research', '0008_auto_20170402_1619'), ('research', '0009_auto_20170403_2350'), ('research', '0010_auto_20170411_2313'), ('research', '0011_auto_20170417_1239'), ('research', '0012_documentarywork_done'), ('research', '0013_auto_20170419_1254')]

    initial = True

    dependencies = [
        ('teams', '0007_auto_20170402_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentaryWork',
            fields=[
                ('team', models.OneToOneField(error_messages={'unique': 'Résultat déjà saisi pour cette équipe.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('jury', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=1, verbose_name='jury')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='heure de passage')),
                ('topic_selection', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='pertinence du sujet')),
                ('documentation', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='travail de documentation')),
                ('presentation', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='qualité de la présentation')),
                ('expression', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='expression orale')),
                ('answers', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='réponses aux questions')),
                ('done', models.BooleanField(default=False, verbose_name='fait')),
                ('evaluation_available', models.BooleanField(default=False, verbose_name='évaluation disponible')),
            ],
            options={
                'verbose_name': 'exposé',
                'ordering': ['team'],
            },
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('team', models.OneToOneField(error_messages={'unique': 'Résultat déjà saisi pour cette équipe.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teams.Team', verbose_name='équipe')),
                ('conformity', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='conformité')),
                ('quality', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='réalisation')),
                ('originality', models.PositiveSmallIntegerField(choices=[(0, '0 - insuffisant'), (1, '1 - médiocre'), (2, '2 - moyen'), (3, '3 - bien'), (4, '4 - très bien')], default=0, verbose_name='originalité')),
            ],
            options={
                'verbose_name': 'poster',
                'ordering': ['team'],
            },
        ),
    ]
