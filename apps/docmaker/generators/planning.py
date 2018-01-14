# -*- coding: utf-8 -*-

import datetime

from django.conf import settings

from reportlab.platypus import Flowable
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape

from docmaker.commons import *

from event.models import Planning

__author__ = 'Eric Pascual'


class PlanningGenerator(ReportGenerator):
    title = 'Planning'
    output_file_name = 'planning'
    description = "global planning"
    page_size = landscape(A4)

    def story(self):
        try:
            for _ in DefaultPageHeader(
                title=self.title,
                page_size=self.page_size
            ).story():
                yield _

            yield PlanningFlowable()

        except GenerationError as e:
            self.add_error(str(e))


class PlanningFlowable(Flowable):
    CHART_X0 = 1.5 * inch
    CHART_Y0 = -0.3 * inch
    DX = 0.25 * inch
    DY = -0.2 * inch

    def __init__(self):
        Flowable.__init__(self)

    @staticmethod
    def _total_minutes(t):
        return t.hour * 60 + t.minute

    def draw(self):
        canvas = self.canv

        base_font = ('Helvetica', 10)
        bars_font = ('Helvetica', 8)

        y = self.CHART_Y0 + 0.4 * inch

        today = datetime.datetime.today().date()

        spans = [_ for _ in zip(*[p.time_span for p in Planning.objects.all()])]
        if not spans:
            raise GenerationError('planning is not yet defined')

        start_time, end_time = [datetime.datetime.combine(today, t) for t in (min(spans[0]), max(spans[1]))]
        # round bounds to the nearest full hour
        start_time = start_time.replace(minute=0)
        end_time = end_time.replace(hour=end_time.hour + 1, minute=0)
        t0_min = self._total_minutes(start_time)
        dt = datetime.timedelta(minutes=settings.PJC['planning_slot_minutes'])

        def _time_to_x(t):
            return (self._total_minutes(t) - t0_min) / 10 * self.DX + self.CHART_X0 - 0.05 * inch

        time = start_time

        y_max = self.CHART_Y0 + (Planning.objects.count() - 1) * self.DY

        label_x_offset = 0.04 * inch
        bar_label_x_offset = 0.06 * inch
        bar_label_y_offset = 0.02 * inch

        canvas.setFont(*base_font)
        while time <= end_time:
            x = _time_to_x(time)

            canvas.saveState()
            canvas.rotate(90)
            canvas.drawCentredString(y, -x - label_x_offset, time.strftime('%H:%M'))
            canvas.restoreState()

            canvas.setStrokeColor(colors.silver)
            canvas.setDash(1, 2)

            canvas.line(x, self.CHART_Y0 - self.DY, x, y_max)

            time += dt

        x_max = x

        x = self.CHART_X0 - 0.2 * inch
        y = self.CHART_Y0

        match_colors = [
            colors.lightpink,
            colors.lightgreen,
            colors.lightblue
        ]
        presentation_color = colors.lightsalmon
        bar_width = -self.DY * 0.6

        for planning in Planning.objects.all():
            team = planning.team

            canvas.setFillColor(colors.black)
            canvas.setFont(*base_font)
            canvas.drawRightString(x, y, "%d - %s" % (team.num, team.name))

            canvas.setStrokeColor(colors.silver)
            canvas.setDash(1, 2)
            y_line = y + bar_width / 2
            canvas.line(self.CHART_X0, y_line, x_max, y_line)

            canvas.setFont(*bars_font)
            for i, match in enumerate(zip(planning.match_times, planning.match_tables)):
                match_time, match_table = match
                bar_x = _time_to_x(match_time)
                canvas.setFillColor(match_colors[i])
                canvas.rect(bar_x, y, self.DX, bar_width, stroke=0, fill=1)
                canvas.setFillColor(colors.black)
                canvas.drawString(bar_x + bar_label_x_offset, y + bar_label_y_offset, "T%s" % match_table)

            bar_x = _time_to_x(planning.presentation_time)
            canvas.setFillColor(presentation_color)
            canvas.rect(bar_x, y, self.DX * 3, bar_width, stroke=0, fill=1)
            canvas.setFillColor(colors.black)
            canvas.drawString(bar_x + bar_label_x_offset, y + bar_label_y_offset, "J%s" % planning.jury)

            y += self.DY

        # draw the legend

        legend_x = self.CHART_X0 + 0.5 * inch
        legend_y = y + self.DY
        x_step = 2 * inch

        canvas.setFont(*base_font)

        x = legend_x
        sample_colors = match_colors + [presentation_color]
        labels = ["épreuve %d" % i for i in range(1, len(match_colors) + 1)] + ['présentation']

        for color, label in zip(sample_colors, labels):
            canvas.setFillColor(color)
            canvas.rect(x - self.DX - 0.1 * inch, legend_y - 0.02 * inch, self.DX, bar_width, stroke=0, fill=1)
            canvas.setFillColor(colors.black)
            canvas.drawString(x, legend_y, label)

            x += x_step

        canvas.drawString(
            legend_x, legend_y + 1.5 * self.DY,
            "(Tn/Jn : n = numéro de table ou de jury)"
        )
