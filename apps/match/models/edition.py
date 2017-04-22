# -*- coding: utf-8 -*-
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from match.models.generic import RoboticsMatch, MSG_COUNTS_MISMATCH, MatchDurationField, MATCH_DURATION

__author__ = 'Eric Pascual'


class Robotics1(RoboticsMatch):
    TRIP_POINTS = 1
    VARIANT_BONUS = 5
    MAX_VARIANTS = 2

    class Meta:
        verbose_name = 'résultat épreuve 1'
        verbose_name_plural = 'résultats épreuve 1'

    trips = models.PositiveSmallIntegerField(
        verbose_name='trajets',
        default=0,
    )
    variants = models.PositiveSmallIntegerField(
        verbose_name='variantes',
        validators=[MaxValueValidator(MAX_VARIANTS)],
        default=0,
    )

    def clean(self):
        if self.variants and self.variants > self.trips - 1:
            raise ValidationError({
                'variants': MSG_COUNTS_MISMATCH,
                'trips': MSG_COUNTS_MISMATCH
            })

    @classmethod
    def mission_complete_credit(cls):
        """ There is not such a concept here, the mission being to do as many travels as possible.
        """
        return None

    def get_points(self):
        """ Counts 1 point per trip and 5 points per variant """
        return self.trips * self.TRIP_POINTS + \
               self.variants * self.VARIANT_BONUS

    def get_detail(self):
        return "trajets : {self.trips}, variantes : {self.variants}".format(self=self)


class Robotics2(RoboticsMatch):
    TRIP_POINTS = 1
    DEPOSITED_POINTS = 4
    INSIDE_AREA_POINTS = 2
    BLOCKS_COUNT = 3

    class Meta:
        verbose_name = 'résultat épreuve 2'
        verbose_name_plural = 'résultats épreuve 2'

    used_time = MatchDurationField(
        verbose_name='temps utilisé',
        default=MATCH_DURATION,
        validators=[validators.MaxValueValidator(MATCH_DURATION)]
    )
    forward_trips = models.PositiveSmallIntegerField(
        verbose_name='trajets aller',
        default=0,
        validators=[validators.MaxValueValidator(BLOCKS_COUNT)]
    )
    return_trips = models.PositiveSmallIntegerField(
        verbose_name='trajets retour',
        default=0,
        validators=[validators.MaxValueValidator(BLOCKS_COUNT)]
    )
    deposited = models.PositiveSmallIntegerField(
        verbose_name='objets déposés',
        default=0,
        validators=[validators.MaxValueValidator(BLOCKS_COUNT)]
    )
    inside = models.PositiveSmallIntegerField(
        verbose_name='objets dans la zone',
        default=0,
        validators=[validators.MaxValueValidator(BLOCKS_COUNT)]
    )

    def clean(self):
        if self.return_trips > self.forward_trips:
            raise ValidationError({
                'forward_trips': MSG_COUNTS_MISMATCH,
                'return_trips': MSG_COUNTS_MISMATCH,
            })
        if self.deposited > self.return_trips:
            raise ValidationError({
                'return_trips': MSG_COUNTS_MISMATCH,
                'deposited': MSG_COUNTS_MISMATCH,
            })
        if self.inside > self.deposited:
            raise ValidationError({
                'inside': MSG_COUNTS_MISMATCH,
                'deposited': MSG_COUNTS_MISMATCH,
            })

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 3 round trips (i.e. 6 trips)
          - 3 valid blocks
        """
        return (cls.TRIP_POINTS * 2 + cls.DEPOSITED_POINTS + cls.INSIDE_AREA_POINTS) * cls.BLOCKS_COUNT

    def get_points(self):
        action_points = self.get_action_points()
        return action_points + self.get_time_bonus(action_points)

    def get_action_points(self):
        return self.forward_trips * self.TRIP_POINTS + \
               self.return_trips * self.TRIP_POINTS + \
               self.deposited * self.DEPOSITED_POINTS + \
               self.inside * self.INSIDE_AREA_POINTS

    def get_time_bonus(self, action_points):
        return int((MATCH_DURATION - self.used_time).total_seconds()) \
            if action_points == self.mission_complete_credit() \
            else 0

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        actions = "allers : {self.forward_trips}, retours : {self.return_trips}, " \
                  "objets déposés : {self.deposited}, objets dans la zone : {self.inside}"\
            .format(self=self)

        return "{actions}, bonus temps : {bonus}".format(actions=actions, bonus=bonus) if bonus else actions


class Robotics3(RoboticsMatch):
    TRIP_POINTS = 2
    MAX_TRIPS = 3
    MOVED_OBSTACLE_PENALTY = 1
    MAX_VARIANTS = 2
    VARIANT_BONUS = 5

    class Meta:
        verbose_name = 'résultat épreuve 3'
        verbose_name_plural = 'résultats épreuve 3'

    trips = models.PositiveSmallIntegerField(
        verbose_name='trajets',
        default=0,
    )
    variants = models.PositiveSmallIntegerField(
        verbose_name='variantes',
        default=0,
    )
    moved_obstacles = models.PositiveSmallIntegerField(
        verbose_name='obstacles déplacés',
        default=0,
    )

    def clean(self):
        if self.variants and self.variants > (self.trips - 1) // 2:
            raise ValidationError({
                "trips": MSG_COUNTS_MISMATCH,
                "variants": MSG_COUNTS_MISMATCH,
            })
        if self.moved_obstacles > self.trips:
            raise ValidationError({
                "trips": MSG_COUNTS_MISMATCH,
                "moved_obstacles": MSG_COUNTS_MISMATCH,
            })

    @classmethod
    def mission_complete_credit(cls):
        """ There is not such a concept here, the mission being to do as many travels as possible.
        """
        return None

    def get_points(self):
        return self.trips * self.TRIP_POINTS + \
               self.variants * self.VARIANT_BONUS - \
               self.moved_obstacles * self.MOVED_OBSTACLE_PENALTY

    def get_detail(self):
        return "trajets : {self.trips}, variantes : {self.variants}, obstacles déplacés : {self.moved_obstacles}"\
            .format(self=self)