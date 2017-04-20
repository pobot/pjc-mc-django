# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models

from teams.models import TeamLinkedModel

__author__ = 'Eric Pascual'
MATCH_DURATION = timedelta(minutes=2, seconds=30)
MSG_COUNTS_MISMATCH = "décomptes non cohérents"


class RoboticsMatch(TeamLinkedModel):
    class Meta:
        abstract = True

    referee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='arbitre',
    )
    time = models.TimeField(
        verbose_name='heure de passage',
        auto_now_add=True,
    )

    def __str__(self):
        return self.team.name

    @classmethod
    def mission_complete_credit(cls):
        raise NotImplementedError()

    def get_points(self):
        raise NotImplementedError()

    points = property(get_points)

    def get_detail(self):
        raise NotImplementedError()

    detail = property(get_detail)

    @property
    def summary(self):
        return "{points} pts ({detail})".format(points=self.get_points(), detail=self.get_detail())


class MatchDurationField(models.DurationField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val is not None:
            seconds = val.seconds
            return '{:02d}:{:02d}'.format(seconds // 60, seconds % 60)
        else:
            return ''