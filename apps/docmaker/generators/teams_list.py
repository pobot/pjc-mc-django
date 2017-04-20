# -*- coding: utf-8 -*-

from reportlab.platypus import Table
from reportlab.lib.units import inch

from docmaker.commons import *

from teams.models import Team

__author__ = 'Eric Pascual'

__all__ = ['TeamsListGenerator']


class TeamsListGenerator(ReportGenerator):
    title = 'Liste des équipes'
    output_file_name = 'teams_list'
    description = "teams list"

    def story(self):
        for _ in DefaultPageHeader(
            title=self.title,
            page_size=self.page_size
        ).story():
            yield _

        yield Table(
            [
                (
                    team.num, team.name, team.grade.abbrev, team.school.name,
                    "%s (%s)" % (team.school.city, team.school.zip_code[:2])
                )
                for team in Team.objects.all()
            ], style=[
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * inch),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * inch),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ])
