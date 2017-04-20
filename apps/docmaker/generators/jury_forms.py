# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Table, ListFlowable
from reportlab.lib.units import inch

from docmaker.commons import *

from research.models import EVALUATION_CHOICES

__author__ = 'Eric Pascual'

__all__ = ['JuryFormGenerator']


class JuryFormGenerator(TeamReportGenerator):
    title = "Dossier de recherche"
    output_file_name = 'jury_forms'
    description = "individual team jury form"

    def body_story(self, team):
        def table_items():
                yield Paragraph(
                    "Pertinence du sujet sélectionné",
                    style=cell_body
                )
                yield Paragraph(
                    "Qualité du travail de documentation",
                    style=cell_body
                )
                yield Paragraph(
                    "Qualité de la présentation",
                    style=cell_body
                )
                yield Paragraph(
                    "Expression orale",
                    style=cell_body
                )
                yield Paragraph(
                    "Réponse aux questions",
                    style=cell_body
                )

        for _ in (
            Table(
                [
                    ['Numéro du jury', '']
                ],
                colWidths=[(6.7 - 2.38) * inch, 2.38 * inch],
                style=default_table_style + [
                    ('BACKGROUND', (0, 0), (0, 0), cell_bkgnd_color),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT')
                ]
            ),
            tables_spacer,
            Paragraph("Noter chaque point ci-dessous en utilisant le barême suivant :", style=cell_body),
            ListFlowable((
              Paragraph(e[1], style=cell_body) for e in EVALUATION_CHOICES
            ), bulletType='bullet', leftIndent=36, bulletDedent=15, spaceBefore=0.1 * inch, start='bulletchar'),
            tables_spacer,
            Table(
                [(_, '') for _ in table_items()],
                colWidths=[6 * inch, 0.7 * inch],
                style=default_table_style + [
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]
            ),
        ):
            yield _
