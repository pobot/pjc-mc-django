# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.core import checks
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from teams.models import TeamLinkedModel

__author__ = 'Eric Pascual'
MATCH_DURATION = timedelta(minutes=2, seconds=30)
MSG_VALUES_MISMATCH = "valeurs incohérentes"


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


class ConstrainedCountField(models.PositiveSmallIntegerField):
    description = _("A counter with min and max limits")

    def __init__(self, min_value=0, max_value=None, **kwargs):
        self.min_value = min_value
        if max_value is None:
            raise ValueError(_('max_value must be specified for a ConstrainedCountField'))
        self.max_value = max_value

        super().__init__(**kwargs)

        # remember limit bindings of validators for later
        self._limit_values = {
            MinValueValidator: self.min_value,
            MaxValueValidator: self.max_value
        }

        # ensure the bound validators are set for the min_value and max_value settings
        not_found_validators = {MinValueValidator, MaxValueValidator}
        for v in self.validators:
            validator_type = type(v)
            if validator_type in self._limit_values:
                v.limit_value = self._limit_values[validator_type]
                not_found_validators.discard(validator_type)

        # add not yet there bound validators
        for v_type in not_found_validators:
            self.validators.append(v_type(limit_value=self._limit_values[v_type]))

        # curate the validators list
        # self._ignored_validators = []
        # validators = []
        # for v in self.validators:
        #     if isinstance(v, (MinValueValidator, MaxValueValidator)):
        #         self._ignored_validators.append(v)
        #     else:
        #         validators.append(v)
        # self._validators = validators
        #
        # # add the bounds validators based on the provided limits
        # self.validators.extend([
        #     MinValueValidator(limit_value=self.min_value),
        #     MaxValueValidator(limit_value=self.max_value),
        # ])

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['min_value'] = self.min_value
        kwargs['max_value'] = self.max_value
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)

        for v in self.validators:
            validator_type = type(v)
            if validator_type in self._limit_values:
                v.limit_value = self._limit_values[validator_type]
        #
        # for v in self._ignored_validators:
        #     v_class = v.__class__.__name__
        #     attr = {
        #         'MinValueValidator': 'min_value',
        #         'MaxValueValidator': 'max_value'
        #     }[v_class]
        #     errors.append(checks.Error(
        #         f'{v_class} cannot be used with ConstrainedCountField (use {attr} kwarg instead).',
        #         obj=self,
        #         id='models.generic.E001',
        #     ))

        return errors

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(ConstrainedCountField, self).formfield(**defaults)
