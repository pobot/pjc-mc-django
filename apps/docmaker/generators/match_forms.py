# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Table, ListFlowable
from reportlab.lib.units import inch

from docmaker.commons import *

__author__ = 'Eric Pascual'


class RoboticsMatchFormGenerator(TeamReportGenerator):
    title = "Robotique"
    output_file_name = 'match_forms'
    description = "individual team match form"

    H_UNIT = 6.7 / 4 * inch

    def _match_header(self, match_num):
        yield Table(
            [
                ['Match', str(match_num), 'Arbitre', '']
            ],
            colWidths=[self.H_UNIT] * 4,
            style=default_table_style + [
                ('BACKGROUND', (0, 0), (0, 0), cell_bkgnd_color),
                ('BACKGROUND', (2, 0), (2, 0), cell_bkgnd_color),
                ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT')
            ]
        )

    def _match1_items(self):
        yield Paragraph(
            "Nombre de trajets aller ou retour",
            style=cell_body
        )
        yield Paragraph(
            "Nombre de variantes (max. 2)",
            style=cell_body
        )

    def _match2_items(self):
        yield Paragraph(
            "Temps restant (mm:ss)",
            style=cell_body
        )
        yield Paragraph(
            "Nombre de trajets aller",
            style=cell_body
        )
        yield Paragraph(
            "Nombre de trajets retour",
            style=cell_body
        )
        yield Paragraph(
            "Nombre d'objets ramenés",
            style=cell_body
        )
        yield Paragraph(
            "Nombre d'objets dans la zone",
            style=cell_body
        )

    def _match3_items(self):
        yield Paragraph(
            "Nombre de trajets aller ou retour",
            style=cell_body
        )
        yield Paragraph(
            "Nombre de variantes (max. 2)",
            style=cell_body
        )
        yield Paragraph(
            "Nombre d'obstacles déplacés (i.e. en partie hors limite)",
            style=cell_body
        )

    def body_story(self, team):
        for ndx, table_items in enumerate([self._match1_items, self._match2_items, self._match3_items]):
            for _ in self._match_header(ndx + 1):
                yield _

            yield Table(
                data=[(_, '') for _ in table_items()],
                colWidths=[3 * self.H_UNIT, self.H_UNIT],
                style=default_table_style + [
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]
            )
            yield tables_spacer
