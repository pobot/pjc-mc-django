# -*- coding: utf-8 -*-

from textwrap import dedent
import argparse
import os

from django.core.management import BaseCommand

from teams.models import Team

__author__ = 'Eric Pascual'

SCRIPT_HOME = os.path.dirname(__file__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.description = dedent("""
            POBOT Web site teams table generator.
            
            Generates the SPIP code for the teams table and copy it in the clipboard
        """)

        parser.formatter_class=argparse.RawTextHelpFormatter

    def handle(self, *args, **options):
        import pyperclip

        lines = [
            '| %(num)d | %(name)s | %(categ)s | %(grade)s | %(school)s | %(city)s | %(dept)0.2s |' % {
                'num': team.num,
                'name': team.name if team.members.count() else '{%s}' % team.name,
                'categ': team.category.name,
                'grade': team.grade_extent_display,
                'school': team.school.name if team.school else '{équipe open}',
                'city': team.school.city if team.school else '',
                'dept': team.school.zip_code[:2] if team.school else ''
            }
            for team in Team.objects.all().order_by('num')
        ]
        pyperclip.copy('\n'.join(lines))

        self.stdout.write("Table code copied in the clipboard.")
