# -*- coding: utf-8 -*-

from enum import Enum

from django.db import models
from django.core import validators


class Display(Enum):
    checkin = 1
    planning = 2
    scores = 3
    next_schedules = 4
    message = 99

    @classmethod
    def next(cls, current):
        if isinstance(current, str):
            current = getattr(cls, current)
            rtype = str
        elif isinstance(current, int):
            current = cls(current)
            rtype = int
        else:
            rtype = cls

        d = ALL_DISPLAYS[(ALL_DISPLAYS.index(current) + 1) % len(ALL_DISPLAYS)]
        if rtype is str:
            return d.name
        if rtype is int:
            return d.value
        return d

    @classmethod
    def next_in_sequence(cls, current, seq, default=None):
        if seq:
            next_display = cls.next(current)
            while next_display not in seq:
                next_display = cls.next(next_display)
        else:
            next_display = default
        return next_display


ALL_DISPLAYS = [Display.checkin, Display.planning, Display.scores, Display.next_schedules]
DISPLAY_NAMES = [d.name for d in ALL_DISPLAYS]


class DisplaySettings(models.Model):
    class Meta:
        app_label = 'display'
        verbose_name = "configuration"
        verbose_name_plural = "configuration"

    delay = models.PositiveSmallIntegerField(
        verbose_name='pause affichage',
        default=5,
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(10)]
    )
    checkin = models.BooleanField(
        verbose_name="pointage",
        default=False
    )
    planning = models.BooleanField(
        verbose_name="planning",
        default=False
    )
    scores = models.BooleanField(
        verbose_name="scores",
        default=False
    )
    next_schedules = models.BooleanField(
        verbose_name="prochains passages",
        default=False
    )
    message = models.CharField(
        verbose_name='message',
        max_length=255,
        blank=True
    )

    def __str__(self):
        return 'Paramètres'

    @property
    def summary(self):
        delay = "pause={delay}s".format(delay=self.delay)
        pages = 'pages=({pages})'.format(pages=', '.join((
            n for n in DISPLAY_NAMES if getattr(self, n)
        )))
        message = 'message="{text}"'.format(text=self.message)
        return ' / '.join((delay, pages, message))

    def current_sequence(self):
        """
        :return: the current display sequence
        :rtype: Display
        """
        seq = [d for d in ALL_DISPLAYS if getattr(self, d.name)]
        return seq or [Display.planning]
