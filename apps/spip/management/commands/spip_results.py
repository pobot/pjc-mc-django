# -*- coding: utf-8 -*-

import os

from event.models import Ranking, RankingType
from teams.models import Team

from .lib import SPIPCommand

__author__ = 'Eric Pascual'

SCRIPT_HOME = os.path.dirname(__file__)


class Command(SPIPCommand):
    description = """
        POBOT Web site results page.
        
        Generates the SPIP code for the tournament final results page and copies it in the clipboard.
    """

    def get_spip_code(self):
        lines = [
            "{{{Les résultats finaux}}}",
            ""
        ]

        def format_general_ranking(entry: Ranking):
            if entry.general == 1:
                fmt = '| {{%(rank)d}}| {{%(name)s}} | %(grade)s | %(school)s |'
            else:
                fmt = '| %(rank)d| %(name)s | %(grade)s | %(school)s |'
            return fmt % {
                'rank': entry.general,
                'name': entry.team.name,
                'grade': entry.team.grade_extent_display,
                'school': school_or_open(entry.team),
            }

        def school_or_open(t: Team):
            return t.school.name if t.school else 'équipe open'

        for categ in (c for c in RankingType if c != RankingType.Scratch):
            qs = Ranking.objects.filter(type_code=categ.value).order_by('general')
            if qs:
                lines.extend([
                    "{{Catégorie %s}}" % categ.name,
                    '',
                    '| {{Rang}} | {{Equipe}} | {{Classe}} | {{Etablissement}} |'
                ])

                lines.extend([format_general_ranking(entry) for entry in qs])
                lines.append('')

        lines.extend([
            '{{{Classement des dossiers de recherche et exposés}}}',
            '',
            '| {{Rang}} | {{Equipe}} |'
        ])
        lines.extend([
            '| %s | %s |' % (entry.research, entry.team.name)
            for entry in Ranking.objects.filter(type_code=RankingType.Scratch.value).order_by('research')
        ])
        lines.append('')

        lines.extend([
            '{{{Classement des affiches}}}',
            '',
            '| {{Rang}} | {{Equipe}} |'
        ])
        lines.extend([
            '| %s | %s |' % (entry.poster, entry.team.name)
            for entry in Ranking.objects.filter(type_code=RankingType.Scratch.value).order_by('poster')
        ])
        lines.append('')

        # qs = Ranking.objects.filter(type_code=RankingType.Scratch.value)
        # lines.extend([
        #     '{{Prix attribués}}',
        #     '',
        #     "| Prix de l'astuce technique | ???? |",
        #     "| Prix de l'exposé | %s |" % qs.order_by('research').first().team.name,
        #     "| Prix de l'affiche | %s |" % qs.order_by('poster').first().team.name,
        #     ''
        # ])

        qs = Team.objects.filter(present=False)
        if qs:
            lines.extend([
                '{{{Forfaits}}}',
                ''
            ])
            lines.extend(['-* %(name)s (%(school)s)' % {
                'name': team.name,
                'school': school_or_open(team),
            } for team in qs])
            lines.append('')

        return lines
