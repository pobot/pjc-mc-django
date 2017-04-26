# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import inch

from docmaker.commons import *

from teams.models import Category

__author__ = 'Eric Pascual'

__all__ = ['ApprovalFormGenerator']


class ApprovalFormGenerator(TeamReportGenerator):
    title = "Fiche d'homologation"
    output_file_name = 'approval_forms'
    description = "individual team approval form"

    items_table_style = default_table_style + [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]

    def body_story(self, team):
        def general_items():
            yield Paragraph(
                "L'équipe a désigné un(e) capitaine qui s'est présenté(e) aux organisateurs",
                style=cell_body
            )
            yield Paragraph(
                "L'équipe a préparé un dossier de recherche sur la thématique de la compétition "
                "et a remis son poster aux organisateurs",
                style=cell_body
            )
            yield Paragraph(
                "L'équipe a bien compris que ne pas se présenter à l'exposé ou ne pas remettre le poster "
                "empêche tout classement dans la compétition",
                style=cell_body
            )
            yield Paragraph(
                "L'équipe a bien compris que ne pas se présenter à une épreuve correspond à un forfait "
                "et qu'elle sera classée derrière toutes les autres pour cette épreuve",
                style=cell_body
            )

        def robotics_items():
                is_mindstorms = team.category == Category.Mindstorms
                yield "Le robot ne comporte qu'une seule %s programmable" % ("brique" if is_mindstorms else 'carte')
                if is_mindstorms:
                    yield Paragraph(
                        "Aucun moyen de solidification <i>(vis, colle, autocollants, adhésif,...)</i> "
                        "n'est utilisé dans la construction du robot",
                        style=cell_body
                    )
                yield Paragraph(
                    "Le robot est entièrement autonome, y compris en matière d'énergie",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe est capable de démontrer qu'elle a parfaitement compris l'utilisation et le principe "
                    "de fonctionnement des capteurs et actionneurs utilisées",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe a bien compris les règles du jeu ainsi que la procédure de départ",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe a bien compris que toute intervention sur le robot pendant le match entraîne "
                    "la disqualification pour l'épreuve",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe est informée que 2 équipiers seulement sont autorisés à être autour de la table de jeu "
                    "pendant les matchs",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe accepte que les décisions des arbitres sont souveraines et qu'aucune contestation "
                    "ne peut être faite après avoir quitté la table de jeu",
                    style=cell_body
                )

        for _ in (
            Table(
                [
                    ['Arbitre', '']
                ],
                colWidths=[6.7 / 2 * inch] * 2,
                style=default_table_style + [
                    ('BACKGROUND', (0, 0), (0, 0), cell_bkgnd_color),
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT')
                ]
            ),
            Paragraph("Déroulement de la compétition", style=section_title),
            Table(
                [(_, '') for _ in general_items()],
                colWidths=[6 * inch, 0.7 * inch],
                style=self.items_table_style
            ),
            Paragraph("Epreuves de robotique", style=section_title),
            Table(
                [(_, '') for _ in robotics_items()],
                colWidths=[6 * inch, 0.7 * inch],
                style=self.items_table_style
            ),
            tables_spacer,
            Paragraph("Signature équipe :", style=section_title),
        ):
            yield _
