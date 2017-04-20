# -*- coding: utf-8 -*-

from match.models.generic import RoboticsMatch
from research.models import DocumentaryWork, Poster
from .models import Ranking

__author__ = 'Eric Pascual'


def result_changed(sender, instance, **kwargs):
    if not isinstance(instance, (RoboticsMatch, DocumentaryWork, Poster)):
        return

    Ranking.compute()
