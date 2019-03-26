# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-26 21:04
from __future__ import unicode_literals

from django.db import migrations, models
import share.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'M'), ('Mme', 'Mme'), ('Mlle', 'Mlle')], default='M', max_length=4, verbose_name='genre')),
                ('first_name', share.fields.FirstNameField(max_length=30, verbose_name='prénom')),
                ('last_name', share.fields.LastNameField(max_length=30, verbose_name='nom')),
                ('email', models.EmailField(max_length=150, verbose_name='email')),
                ('status', models.CharField(choices=[('?', 'pas de réponse'), ('P', 'Présent(e)'), ('A', 'Absent(e)')], default='?', max_length=1, verbose_name='statut')),
                ('present', models.BooleanField(default=False, verbose_name='présent(e)')),
            ],
            options={
                'verbose_name': 'volontaire',
                'verbose_name_plural': 'volontaires',
                'ordering': ['last_name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='volunteer',
            unique_together=set([('first_name', 'last_name')]),
        ),
    ]