# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20171105_0004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamcontact',
            options={'ordering': ['last_name'], 'verbose_name': 'contact', 'verbose_name_plural': 'contacts'},
        ),
        # migrations.AlterField(
        #     model_name='teamcontact',
        #     name='gender',
        #     field=models.CharField(choices=[('M', 'M'), ('Mme', 'Mme'), ('Mlle', 'Mlle')], default='M', max_length=4, verbose_name='genre'),
        # ),
    ]
