# -*- coding: utf-8 -*-

import os

from django.conf import settings

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color, black, lightgrey
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image

from docmaker.commons import ASSETS_DIR, ReportGenerator

from teams.models import Team

__author__ = 'Eric Pascual'

__all__ = ['DiplomasGenerator']

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2


class DiplomasGenerator(ReportGenerator):
    title = "Diplômes et certificats"
    output_file_name = 'diplomas'
    description = "diplomas and certificates for teams"
    page_width, page_height = page_size = landscape(A4)

    frame_width = 730
    frame_height = 500
    frame_x0 = (page_width - frame_width) / 2
    frame_y0 = (page_height - frame_height) / 2

    frame_bkgnd_color = HexColor(0xe5eaef)

    def __init__(self, output_dir):
        super().__init__(output_dir)

        self.logo_path = os.path.join(ASSETS_DIR, "logo_left.png")
        self.logo_size = Image.open(self.logo_path).size

        self.canvas = None

    def _draw_text(self,
                   text: str,
                   x: float, y: float,
                   color: Color,
                   font_name: str,
                   font_size: int,
                   align: int = ALIGN_LEFT,
                   char_space: float = 0
                   ):
        if align != ALIGN_LEFT:
            sw = pdfmetrics.stringWidth(text, font_name, font_size) + char_space * (len(text) - 1)
            if align == ALIGN_CENTER:
                x -= sw / 2
            else:
                x -= sw
        text_obj = self.canvas.beginText(x=x, y=y)
        text_obj.setFont(font_name, font_size)
        text_obj.setCharSpace(char_space)
        text_obj.setStrokeColor(color)
        text_obj.setFillColor(color)
        text_obj.textLine(text)
        self.canvas.drawText(text_obj)

    def _draw_frame(self, frame_color, title):
        self.canvas.setFillColor(self.frame_bkgnd_color)
        self.canvas.setStrokeColor(HexColor(frame_color))
        self.canvas.setLineWidth(20)
        self.canvas.roundRect(
            x=self.frame_x0, y=self.frame_y0,
            width=self.frame_width, height=self.frame_height,
            radius=10,
            stroke=1, fill=1
        )

        self._draw_text(
            settings.PJC['title_long'],
            x=self.page_width / 2,
            y=self.frame_height,
            color=HexColor(0x800000),
            font_name="DejaVuSansCondensed-Bold", font_size=36,
            align=ALIGN_CENTER,
            char_space=-2.5
        )

        self._draw_text(
            title,
            x=self.page_width / 2,
            y=self.frame_height * 0.80,
            color=black,
            font_name="Sverige", font_size=55,
            align=ALIGN_CENTER
        )

        self._draw_text(
            "décerné à l'équipe",
            x=self.page_width / 2,
            y=self.frame_height * 0.65,
            color=black,
            font_name="DejaVuSans-Normal", font_size=16,
            align=ALIGN_CENTER
        )

        self._draw_text(
            "à Valbonne, Alpes-Maritimes le %s" % settings.PJC['event_date'],
            x=self.page_width * 0.66,
            y=self.frame_height * 0.25,
            color=black,
            font_name="DejaVuSans-Normal", font_size=16,
            align=ALIGN_CENTER
        )

        logo_display_w, logo_display_h = (round(d * 0.75) for d in self.logo_size)
        self.canvas.drawImage(
            self.logo_path,
            x=self.frame_x0 + 25, y=self.frame_y0 + 25,
            width=logo_display_w, height=logo_display_h,
            mask='auto'
        )

    def _generate_participation_certificates(self, teams):
        for team in Team.objects.all():
            self._draw_frame(frame_color=0xbba62f, title="Certificat de Participation")

            self._draw_text(
                team.name,
                self.page_width / 2,
                self.frame_height * 0.55,
                black,
                "DejaVuSansCondensed-Bold", 32,
                ALIGN_CENTER
            )

            self.canvas.showPage()

    def _generate_diploma(self, frame_color, title):
        self._draw_frame(frame_color=frame_color, title=title)

        self.canvas.setStrokeColor(lightgrey)
        self.canvas.setLineWidth(1)
        y = self.frame_height * 0.50
        x0 = self.page_width / 2
        line_length = self.frame_width * 0.6
        self.canvas.line(x0 - line_length / 2, y, x0 + line_length / 2, y)

        self.canvas.showPage()

    def _generate_presentation_diploma(self):
        self._generate_diploma(frame_color=0x2fbb4b, title="Prix du Meilleur Exposé")

    def _generate_poster_diploma(self):
        self._generate_diploma(frame_color=0x2f6bbb, title="Prix du Meilleur Poster")

    def _generate_robot_diploma(self):
        self._generate_diploma(frame_color=0xbb2f30, title="Prix du Meilleur Robot")

    def generate(self):
        self.canvas = canvas.Canvas(
            self.pdf_file_path,
            pagesize=self.page_size
        )

        for font_name, font_file in [
            ("DejaVuSansCondensed-Bold", "DejaVuSansCondensed-Bold.ttf"),
            ("DejaVuSans-Normal", "DejaVuSans.ttf"),
            ("Sverige", "SverigeScriptDecorated_Demo.ttf")
        ]:
            pdfmetrics.registerFont(TTFont(font_name, os.path.join(ASSETS_DIR, font_file)))

        self._generate_participation_certificates(Team.objects.all())
        self._generate_presentation_diploma()
        self._generate_poster_diploma()
        self._generate_robot_diploma()

        self.canvas.save()

