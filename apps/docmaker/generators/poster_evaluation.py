# -*- coding: utf-8 -*-

from reportlab.platypus import Table, Paragraph, ListFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors

from docmaker.commons import *

from teams.models import Team
from research.models import EVALUATION_CHOICES

__author__ = 'Eric Pascual'

__all__ = ['PostersEvalGridGenerator']


class PostersEvalGridGenerator(ReportGenerator):
    title = 'Grille évaluation posters'
    output_file_name = 'posters_eval_grid'
    description = "posters evaluation grid"

    H_UNIT = 6.7 / 6 * inch

    def story(self):
        for _ in DefaultPageHeader(
            title=self.title,
            page_size=self.page_size
        ).story():
            yield _
        for _ in (
            Paragraph("Noter chaque critère d'évaluation du poster en utilisant le barême suivant :", style=cell_body),
            Table(
                [[e[1] for e in EVALUATION_CHOICES]],
                colWidths=[self.H_UNIT] * 5,
                style=[
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                ]
            ),
            tables_spacer,
            Table(
                [
                    ("", "Conformité", "Qualité", "Originalité")
                ] +
                [
                    (
                        "%d - %s" % (team.num, team.name), "", "", ""
                    )
                    for team in Team.objects.all()
                ],
                colWidths=[self.H_UNIT * 3, self.H_UNIT, self.H_UNIT, self.H_UNIT],
                style=no_grid_table_style + [
                    ('GRID', (0, 1), (-1, -1), 0.5, colors.black),
                    ('TOPPADDING', (0, 0), (-1, -1), 0.1 * inch),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * inch),
                    ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
                ]),
        ):
            yield _
