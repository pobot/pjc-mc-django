# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import inch

from docmaker.commons import *

from teams.models import Category

__author__ = 'Eric Pascual'

__all__ = ['ApprovalSheetGenerator']


class ApprovalSheetGenerator(TeamReportGenerator):
    title = "Fiche d'homologation"
    output_file_name = 'approval_sheets'
    description = "individual approval sheet"

    def body_story(self, team):
        def table_items():
                is_mindstorms = team.category == Category.Mindstorms
                yield "Le robot ne comporte qu'une seule %s programmable" % ("brique" if is_mindstorms else 'carte')
                if is_mindstorms:
                    yield Paragraph(
                        "Aucun moyen de solidification du robot <i>(vis, colle, autocollants, adhésif,...)</i> "
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
                    "L'équipe a préparé un dossier de recherche sur la thématique de la compétition "
                    "et a remis son poster aux organisateurs",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe a bien compris les règles du jeu ainsi que la procédure de départ",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe est informée que 2 équipiers seulement sont autorisés à être autour de la table de jeu "
                    "pendant les matchs",
                    style=cell_body
                )
                yield Paragraph(
                    "L'équipe a bien compris que toute intervention sur le robot pendant le match entraîne "
                    "la disqualification pour l'épreuve",
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
            tables_spacer,
            Table(
                [(_, '') for _ in table_items()],
                colWidths=[6 * inch, 0.7 * inch],
                style=default_table_style + [
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]
            ),
            tables_spacer,
            Table(
                [
                    ['Signature équipe :', '']
                ],
                colWidths=[6.7 / 2 * inch] * 2,
                style=no_grid_table_style + [
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                ]
            ),

        ):
            yield _
