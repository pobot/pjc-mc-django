# -*- coding: utf-8 -*-
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from match.models.generic import RoboticsMatch, MSG_COUNTS_MISMATCH, MatchDurationField, MATCH_DURATION

__author__ = 'Eric Pascual'


class TravelledDistanceMatch(RoboticsMatch):
    QUADRANT_POINTS = 1

    class Meta:
        abstract = True

    quadrants = models.PositiveSmallIntegerField(
        verbose_name='quadrants',
        default=0,
    )

    def get_points(self):
        """ Counts 1 point per full quadrant """
        return self.quadrants * self.QUADRANT_POINTS

    def get_detail(self):
        return f"quadrants : {self.quadrants}"


class Robotics1(TravelledDistanceMatch):
    class Meta:
        verbose_name = 'résultat épreuve 1'
        verbose_name_plural = 'résultats épreuve 1'


class Robotics2(TravelledDistanceMatch):
    MOVED_OBSTACLE_PENALTY = 1

    class Meta:
        verbose_name = 'résultat épreuve 2'
        verbose_name_plural = 'résultats épreuve 2'

    moved_obstacles = models.PositiveSmallIntegerField(
        verbose_name='obstacles déplacés',
        default=0,
    )

    def clean(self):
        super().clean()
        if self.moved_obstacles > self.quadrants / 2 + 1:
            raise ValidationError({
                'quadrants': MSG_COUNTS_MISMATCH,
                'moved_obstacles': MSG_COUNTS_MISMATCH,
            })

    def get_points(self):
        return super().get_points() - self.moved_obstacles * self.MOVED_OBSTACLE_PENALTY

    def get_detail(self):
        return f"quadrants : {self.quadrants}, objets déplacés: {self.moved_obstacles}"


class Robotics3(TravelledDistanceMatch):
    class Meta:
        verbose_name = 'résultat épreuve 3'
        verbose_name_plural = 'résultats épreuve 3'
