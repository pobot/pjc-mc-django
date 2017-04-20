# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
from django.db import connection, transaction
from django.db.models.deletion import ProtectedError

from teams.models import School

__author__ = 'Eric Pascual'


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                School.objects.all().delete()

                cursor = connection.cursor()
                cursor.execute('update sqlite_sequence set seq=0 WHERE name = "teams_school"')

                School.objects.bulk_create((
                    School(name='Collège International de Valbonne', city='SOPHIA ANTIPOLIS', zip_code='06560'),
                    School(name='Lycée International de Valbonne', city='SOPHIA ANTIPOLIS', zip_code='06560'),
                    School(name='Lycée St Joseph', city='HASPARREN', zip_code='64240'),
                    School(name='Lycée du Pays de Soule', city='CHERAUTE', zip_code='64130'),
                    School(name='Collège Louis Nucera', city='NICE', zip_code='06000'),
                    School(name='Collège Emile Roux', city='LE CANNET', zip_code='06160'),
                    School(name='Collège St Philippe Neri', city='JUAN LES PINS', zip_code='06110'),
                    School(name='Collège Rolland Garros', city='NICE', zip_code='06000'),
                ))
        except ProtectedError as e:
            self.stderr.write('Cannot clear School instances since related objects exist.')
        else:
            self.stdout.write('Done.')
