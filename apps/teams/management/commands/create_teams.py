# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
from django.db import connection

from teams.models import School, Team, Grade, Category

__author__ = 'Eric Pascual'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Team.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('update sqlite_sequence set seq=0 WHERE name = "teams_team"')

        teams = []

        lycee_pays_de_soule = School.objects.get(name="Lycée du Pays de Soule")
        teams.extend([
            Team(name="Castanha Shüta", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
            Team(name="The Saving Family", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
            Team(name="Réunion Basci-Béarnais", grade=Grade.premiere, category=Category.Mindstorms, school=lycee_pays_de_soule),
        ])

        liv = School.objects.get(name="Lycée International de Valbonne")
        teams.extend([
            Team(name="Playbot", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="BRUH", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Robot Jul", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Wizzbot", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Green Studio", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Blank", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Echo", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
            Team(name="Gear", grade=Grade.seconde, category=Category.Mindstorms, school=liv),
        ])

        civ = School.objects.get(name="Collège International de Valbonne")
        teams.extend([
            Team(name="Robot55 Team", grade=Grade.cinquieme, category=Category.Arduino, school=civ),
            Team(name="Robot56 Team", grade=Grade.cinquieme, category=Category.Arduino, school=civ),
        ])

        st_joseph = School.objects.get(name="Lycée St Joseph")
        teams.extend([
            Team(name="PoweRobot", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
            Team(name="Securi-Bot", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
            Team(name="SEJO Haspatech", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
            Team(name="EuskalRobota", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
            Team(name="Azkargeek", grade=Grade.seconde, category=Category.Mindstorms, school=st_joseph),
        ])

        st_ph_neri = School.objects.get(name="Collège St Philippe Neri")
        teams.extend([
            Team(name="Les Nerissons", grade=Grade.sixieme, category=Category.Mindstorms, school=st_ph_neri),
        ])

        emile_roux = School.objects.get(name="Collège Emile Roux")
        teams.extend([
            Team(name="Emibot 1.0", grade=Grade.quatrieme, category=Category.Mindstorms, school=emile_roux),
            Team(name="Emibot 2.0", grade=Grade.cinquieme, category=Category.Arduino, school=emile_roux),
        ])

        Team.objects.bulk_create(teams)

        self.stdout.write('%d teams created:' % Team.objects.count())
        for team in Team.objects.all():
            self.stdout.write('- %s (%s) - %s' % (team, team.grade.abbrev, team.school))
