# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password

__author__ = 'Eric Pascual'

REFEREES_GROUP_NAME = 'arbitres'

REFEREES = [
    ('Fabrice', 'Fabrice', 'Rubino'),
    ('FredM', 'Frédéric', 'Maria'),
    ('FredR', 'Frédéric', 'Rallo'),
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        referee_permissions = Permission.objects.filter(
            codename__contains="robotics"
        ).exclude(codename__startswith="delete")

        try:
            ref_group = Group.objects.get(name=REFEREES_GROUP_NAME)
        except Group.DoesNotExist:
            print(f'Creating group {REFEREES_GROUP_NAME}...')
            ref_group = Group.objects.create(
                name=REFEREES_GROUP_NAME
            )
            ref_group.permissions = referee_permissions
            print('... ok')
        else:
            print(f'The group {REFEREES_GROUP_NAME} already exists.')

        print("Creating users...")

        for username, first_name, last_name in REFEREES:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=make_password('pobot4ever')
                )
                user.groups.add(ref_group)
                print(f'User {username} created and added to referees group.')
            else:
                print(f'User {username} ({user.first_name} {user.last_name}) already exists.')
