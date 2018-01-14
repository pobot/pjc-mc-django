# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Table, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from docmaker.commons import *

__author__ = 'Eric Pascual'

__all__ = ['StandLabelGenerator']


class CustomTeamHeader(DefaultTeamHeader):
    team_num_style = ParagraphStyle(
        'label_team_num',
        fontSize=48,
        autoLeading='min',
        alignment=TA_CENTER,
    )

    team_name_style = ParagraphStyle(
        'label_team_name',
        parent=team_num_style,
        fontName="Helvetica-Oblique",
        fontSize=40,
        wordWrap=False,
        spaceBefore=0.3 * inch,
        leftIndent=-1 * inch,  # increase margins to avoid long team names wrapping
        rightIndent=-1 * inch,
    )

    team_detail_style = ParagraphStyle(
        'label_team_detail',
        parent=team_name_style,
        fontSize=24,
        autoLeading='min',
    )

    def story(self):
        for _ in (
            Paragraph('Equipe %d' % self._team.num, self.team_num_style),
            Paragraph(self._team.name, self.team_name_style),
            Spacer(0, .5 * inch),
            Paragraph(self._team.school.name if self._team.school else '<i>équipe open</i>', self.team_detail_style),
            Paragraph(self._team.grade_extent_display, self.team_detail_style),
            Paragraph("%s (%s)" % (self._team.school.city, self._team.school.zip_code[:2]), self.team_detail_style),
            Spacer(0, 0.5 * inch),
            Paragraph(
                "Catégorie : %s" % self._team.category.name, self.team_category_style
            ),
            Spacer(0, 1 * inch)
        ):
            yield _


class StandLabelGenerator(TeamReportGenerator):
    title = "Etiquette de stand"
    print_title = False
    output_file_name = 'stand_labels'
    description = "team stand label"
    team_header_class = CustomTeamHeader

    time_table_header_style = ParagraphStyle(
        'label_time_table_header',
        parent=cell_header,
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=0.3 * inch
    )

    def body_story(self, team):
        try:
            for _ in (
                Paragraph(
                    "Heures de passage", self.time_table_header_style
                ),
                Table(
                    [
                        [
                            'Epreuve %d' % (i + 1),
                            t[0].strftime('%H:%M'),
                            'Table',
                            t[1]
                        ] for i, t in enumerate(zip(team.planning.match_times, team.planning.match_tables))
                    ],
                    colWidths=[6.7 / 4 * inch] * 4,
                    style=default_table_style + [
                        ('BACKGROUND', (0, 0), (0, -1), cell_bkgnd_color),
                        ('BACKGROUND', (2, 0), (2, -1), cell_bkgnd_color),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                    ]
                ),
                tables_spacer,
                Table(
                    [
                        [
                            'Exposé',
                            team.planning.presentation_time.strftime('%H:%M'),
                            'Jury',
                            team.planning.jury
                        ]
                    ],
                    colWidths=[6.7 / 4 * inch] * 4,
                    style=default_table_style + [
                        ('BACKGROUND', (0, 0), (0, -1), cell_bkgnd_color),
                        ('BACKGROUND', (2, 0), (2, -1), cell_bkgnd_color),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                    ]
                )
            ):
                yield _

        except Exception:
            raise GenerationError('planning is not yet defined')


