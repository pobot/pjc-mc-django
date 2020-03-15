# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

from match.models.generic import (
    RoboticsMatch,
    MatchDurationField, ConstrainedCountField,
    MSG_VALUES_MISMATCH, MATCH_DURATION,
)

__author__ = 'Eric Pascual'

# IMPORTANT NOTICE
#
# Never declare a match model as derived from another one. This will defeat the
# refereeing forms automatic creation due to missing the relation between the team
# and the class of this match model (the relation will be considered with the parent
# class and not the class itself).
#
# Use abstract models instead for shared fields, and always use "final" classes
# for match models.


class BaseMatch(RoboticsMatch):
    class Meta:
        abstract = True

    used_time = MatchDurationField(
        verbose_name='temps utilisé',
        validators=[validators.MaxValueValidator(MATCH_DURATION - timedelta(seconds=1))]
    )

    @classmethod
    def mission_complete_credit(cls):
        raise NotImplementedError()

    def get_time_bonus(self, action_points):
        return int((MATCH_DURATION - self.used_time).total_seconds()) \
            if action_points == self.mission_complete_credit() \
            else 0

    def get_action_points(self):
        raise NotImplementedError()

    def get_points(self):
        action_points = self.get_action_points()
        return action_points + self.get_time_bonus(action_points)


class TravelCountBasedMatch(BaseMatch):
    TRAVEL_POINTS = 1
    MAX_TRAVELS = 6

    class Meta:
        abstract = True

    travels = ConstrainedCountField(
        verbose_name='trajets effectués',
        default=0,
        max_value=MAX_TRAVELS,
    )

    def get_action_points(self):
        """ Counts 1 point per travel """
        return self.travels * self.TRAVEL_POINTS


class Robotics1(TravelCountBasedMatch):
    class Meta:
        verbose_name = 'résultat épreuve 1'
        verbose_name_plural = 'résultats épreuve 1'

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 6 travels done
        """
        return cls.TRAVEL_POINTS * cls.MAX_TRAVELS

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return f"trajets : {self.travels}, bonus temps : {bonus}"


class Robotics2(TravelCountBasedMatch):
    MOVED_OBSTACLE_MALUS = 5
    OBSTACLE_COUNT = 3

    class Meta:
        verbose_name = 'résultat épreuve 2'
        verbose_name_plural = 'résultats épreuve 2'

    moved_obstacles = ConstrainedCountField(
        verbose_name='obstacle déplacés',
        default=0,
        max_value=OBSTACLE_COUNT,
    )

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 6 travels done
          - no obstacle moved
        """
        return cls.TRAVEL_POINTS * cls.MAX_TRAVELS

    def get_action_points(self):
        return super().get_action_points() - self.MOVED_OBSTACLE_MALUS * self.moved_obstacles

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return f"trajets : {self.travels}, obstacles déplacés : {self.moved_obstacles}, bonus temps : {bonus}"

    _moved_limits = [1, 1, 1, 2, 2, 3, 3]

    def clean(self):
        if self.moved_obstacles > self._moved_limits[self.travels]:
            raise ValidationError({
                'travels': MSG_VALUES_MISMATCH,
                'moved_obstacles': MSG_VALUES_MISMATCH
            })


class Robotics3(BaseMatch):
    FRUITS_COLLECTED_SINGLE_BONUS = 1
    GOOD_FRUIT_BONUS = 1
    BAD_FRUIT_MALUS = 2

    MAX_GOOD_FRUITS = 6
    MAX_BAD_FRUITS = 3

    class Meta:
        verbose_name = 'résultat épreuve 3'
        verbose_name_plural = 'résultats épreuve 3'

    good_fruits = ConstrainedCountField(
        verbose_name='fruits mûrs',
        default=0,
        max_value=MAX_GOOD_FRUITS
    )
    bad_fruits = ConstrainedCountField(
        verbose_name='fruits verts',
        default=0,
        max_value=MAX_BAD_FRUITS
    )

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 6 good fruits picked and at home
          - no bad fruits picked
        """
        return cls.MAX_GOOD_FRUITS * cls.GOOD_FRUIT_BONUS + cls.FRUITS_COLLECTED_SINGLE_BONUS

    def get_action_points(self):
        return \
            (1 if self.good_fruits or self.bad_fruits else 0) + \
            self.GOOD_FRUIT_BONUS * self.good_fruits - \
            self.BAD_FRUIT_MALUS * self.bad_fruits

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return \
            f"fruits mûrs : {self.good_fruits}" \
            f", fruits verts : {self.bad_fruits}" \
            f", bonus temps : {bonus}"
