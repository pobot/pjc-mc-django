# -*- coding: utf-8 -*-

from match.models.generic import RoboticsMatch
from research.models import DocumentaryWork, Poster


__author__ = 'Eric Pascual'


def result_saved(sender, instance, **kwargs):
    if not isinstance(instance, (RoboticsMatch, DocumentaryWork, Poster)):
        return

    team = instance.team
    team.present = True
    team.save()
