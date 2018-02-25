# -*- coding: utf-8 -*-

from reportlab.platypus import Table
from reportlab.lib.units import inch

from docmaker.commons import *

__author__ = 'Eric Pascual'


__all__ = ['TeamRegistrationFormGenerator']


def pretty_phone_number(s):
    if ' ' in s:
        return s

    return ' '.join(s[i:i+2] for i in range(0, 10, 2))


class TeamRegistrationFormGenerator(TeamReportGenerator):
    title = "Formulaire d'inscription"
    output_file_name = 'team_registration_forms'
    description = "team registration forms"

    H_UNIT = 6.7 / 6 * inch

    def body_story(self, team):
        for _ in (
            Table(
                [
                    ("Contact", team.contact.full_name),
                    ("Email", team.contact.email),
                    ("Téléphone", pretty_phone_number(team.contact.phone_number)),
                ],
                colWidths=[self.H_UNIT * 3] * 2,
                style=no_grid_table_style + [
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 0.1 * inch),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ]
            ),
            tables_spacer,
            Table(
                [
                    ("Nom, prénom", "Classe", "Date de naissance")
                ] +
                [
                    (
                        member.last_name + ' ' + member.first_name,
                        member.grade.label, member.birth_date.strftime('%d/%m/%Y')
                    )
                    for member in team.members.all().order_by('last_name')
                ],
                colWidths=[self.H_UNIT * 3, self.H_UNIT, self.H_UNIT * 2],
                style=no_grid_table_style + [
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('TOPPADDING', (0, 0), (-1, -1), 0.1 * inch),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ]),
        ):
            yield _
