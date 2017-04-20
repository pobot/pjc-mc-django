# -*- coding: utf-8 -*-

import os
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, Image, ListFlowable, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

from teams.models import Team

__author__ = 'Eric Pascual'

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../resources')    # TODO replace by pkg way

logo_left = Image(os.path.join(ASSETS_DIR, 'logo_left.png'), width=0.84 * inch, height=0.79 * inch)
logo_right = Image(os.path.join(ASSETS_DIR, 'logo_right.png'), width=0.95 * inch, height=0.79 * inch)


class PJCDocTemplate(SimpleDocTemplate):
    # declare these attributes for Lint not to complain, since created by setattr in the base class
    timestamp = text_x = text_y = pagesize = rightMargin = bottomMargin = None

    def handle_documentBegin(self):
        super().handle_documentBegin()

        self.timestamp = datetime.datetime.now().strftime("Généré le %d/%m/%Y à %H:%M:%S")
        self.text_x = self.pagesize[0] - self.rightMargin / 2
        self.text_y = self.bottomMargin / 2

    def handle_pageEnd(self):
        canvas = self.canv
        canvas.setFillColor(colors.black)
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(self.text_x, self.text_y, self.timestamp)

        super().handle_pageEnd()


class ReportGenerator(object):
    title = None
    output_file_name = None
    page_size = portrait(A4)

    def __init__(self, output_dir):
        self._output_dir = output_dir

    def generate(self):
        pdf_file_path = os.path.join(self._output_dir, self.output_file_name + '.pdf')
        pdf_doc = PJCDocTemplate(
            filename=pdf_file_path,
            pagesize=self.page_size,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            title="POBOT Junior Cup " + self.title,
            author="POBOT"
        )
        doc_story = self.get_story()
        pdf_doc.build(doc_story)

    def get_story(self):
        raise NotImplementedError()


class PageHeader(object):
    LOGO_WIDTH = 1.15 * inch
    MARGIN = 0.5 * inch

    def __init__(self, title=None, page_size=portrait(A4)):
        self.title = title or ''
        self.text_width = page_size[0] - 2 * self.MARGIN

    def story(self):
        for _ in (
            Table(
                data=[
                    [logo_left, 'POBOT Junior Cup 2017', logo_right],       # TODO replace year literal by setting parm
                    ['', self.title, '']
                ],
                colWidths=[self.LOGO_WIDTH, self.text_width - 2 * self.LOGO_WIDTH, self.LOGO_WIDTH],
                rowHeights=[0.5 * inch, 0.5 * inch],
                style=[
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 24),
                    ('FONTSIZE', (0, 1), (2, 1), 18),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('VALIGN', (1, 0), (1, -1), 'TOP'),
                    ('SPAN', (0, 0), (0, 1)),
                    ('SPAN', (2, 0), (2, 1)),
                ]
            ),
            Spacer(0, 0.5 * inch)
        ):
            yield _


class TeamHeader(object):
    team_name_style = ParagraphStyle(
        'team_name',
        fontName='Helvetica-Bold',
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=0.2 * inch
    )

    team_school_style = ParagraphStyle(
        'team_school',
        fontName='Helvetica',
        fontSize=14,
        alignment=TA_CENTER
    )

    def __init__(self, team):
        self._team = team

    def story(self):
        for _ in (
            Paragraph("%s - %s" % (self._team.num, self._team.name), self.team_name_style),
            Paragraph(
                "%s - %s" % (self._team.school or '<i>équipe open</i>', self._team.grade.orig),
                self.team_school_style
            ),
            Spacer(0, 0.5 * inch)
        ):
            yield _


class TeamReportGenerator(ReportGenerator):
    def get_story(self):
        page_header = PageHeader(title=self.title, page_size=self.page_size)

        for team in Team.objects.all():
            for _ in page_header.story():
                yield _

            team_header = TeamHeader(team)
            for _ in team_header.story():
                yield _

            for _ in self.body_story(team):
                yield _

            yield PageBreak()

    def body_story(self, team):
        raise NotImplementedError()
