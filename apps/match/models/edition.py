# -*- coding: utf-8 -*-
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from match.models.generic import RoboticsMatch, MSG_COUNTS_MISMATCH, MatchDurationField, MATCH_DURATION

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
        default=MATCH_DURATION,
        validators=[validators.MaxValueValidator(MATCH_DURATION)]
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


class SectionBasedMatch(BaseMatch):
    SECTION_POINTS = 1
    MAX_SECTIONS = 8

    class Meta:
        abstract = True

    sections = models.PositiveSmallIntegerField(
        verbose_name='sections parcourues',
        default=0,
        validators=[MaxValueValidator(limit_value=MAX_SECTIONS)]
    )

    def get_action_points(self):
        """ Counts 1 point per full section """
        return self.sections * self.SECTION_POINTS


class Robotics1(SectionBasedMatch):
    class Meta:
        verbose_name = 'résultat épreuve 1'
        verbose_name_plural = 'résultats épreuve 1'

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 8 sections traveled
        """
        return cls.SECTION_POINTS * cls.MAX_SECTIONS

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return f"sections : {self.sections}, bonus temps : {bonus}"


class Robotics2(SectionBasedMatch):
    OBJECT_RETRIEVED_POINTS = 5

    class Meta:
        verbose_name = 'résultat épreuve 2'
        verbose_name_plural = 'résultats épreuve 2'

    object_retrieved = models.BooleanField(
        verbose_name='objet récupéré',
        default=False,
    )

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 8 sections traveled
          - object retrieved
        """
        return super().mission_complete_credit() + cls.OBJECT_RETRIEVED_POINTS

    def get_action_points(self):
        return super().get_action_points() + (self.OBJECT_RETRIEVED_POINTS if self.object_retrieved else 0)

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return f"sections : {self.sections}, objet récupéré : {self.object_retrieved}, bonus temps : {bonus}"


class Robotics3(BaseMatch):
    OBJECT_CAPTURED_POINTS = 1
    OBJECT_DEPOSITED_POINTS = 2

    MAX_OBJECTS = 2

    class Meta:
        verbose_name = 'résultat épreuve 3'
        verbose_name_plural = 'résultats épreuve 3'

    captured_objects = models.PositiveSmallIntegerField(
        verbose_name='objets récupérés',
        default=0,
        validators=[MaxValueValidator(limit_value=MAX_OBJECTS)]
    )
    deposited_objects = models.PositiveSmallIntegerField(
        verbose_name='objets déposés',
        default=0,
        validators=[MaxValueValidator(limit_value=MAX_OBJECTS)]
    )

    def clean(self):
        if self.deposited_objects > self.captured_objects:
            raise ValidationError({
                'captured_objects': MSG_COUNTS_MISMATCH,
                'deposited_objects': MSG_COUNTS_MISMATCH
            })

    @classmethod
    def mission_complete_credit(cls):
        """ The max action credits corresponds to :
          - 2 objects captured and deposited
        """
        return cls.MAX_OBJECTS * (cls.OBJECT_CAPTURED_POINTS + cls.OBJECT_DEPOSITED_POINTS)

    def get_action_points(self):
        return \
            self.OBJECT_CAPTURED_POINTS * self.captured_objects + \
            self.OBJECT_DEPOSITED_POINTS * self.deposited_objects

    def get_detail(self):
        bonus = self.get_time_bonus(self.get_action_points())
        return \
            f"objets capturés : {self.captured_objects}" \
            f", objets déposés : {self.deposited_objects}" \
            f", bonus temps : {bonus}"
