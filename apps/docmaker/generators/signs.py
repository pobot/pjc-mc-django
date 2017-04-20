# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

from docmaker.commons import *

__author__ = 'Eric Pascual'

__all__ = ['SignsGenerator']


class SignsGenerator(ReportGenerator):
    title = 'Signalétique'
    output_file_name = 'signs'
    description = "table and jury signs"
    page_size = landscape(A4)

    def story(self):
        big_letters = ParagraphStyle(
            'big_letters',
            fontSize=120,
            alignment=TA_CENTER,
        )

        page_header = DefaultPageHeader(
            title=None,
            page_size=self.page_size
        )

        for table_num in range(1, 4):
            for side in range(4):
                for _ in page_header.story():
                    yield _

                for _ in (
                    Spacer(0, 1 * inch),
                    Paragraph("Table %d" % table_num, big_letters),
                    PageBreak()
                ):
                    yield _

        for jury_num in range(1, 4):
            for _ in page_header.story():
                yield _

            for _ in (
                Spacer(0, 1 * inch),
                Paragraph("Jury %d" % jury_num, big_letters),
                PageBreak()
            ):
                yield _
