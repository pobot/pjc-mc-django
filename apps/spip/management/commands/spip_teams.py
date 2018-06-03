# -*- coding: utf-8 -*-

import os

from teams.models import Team

from .lib import SPIPCommand

__author__ = 'Eric Pascual'

SCRIPT_HOME = os.path.dirname(__file__)


class Command(SPIPCommand):
    description = """
        POBOT Web site teams table generator.
        
        Generates the SPIP code for the teams table and copies it in the clipboard.
    """

    def get_spip_code(self):
        return [
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
