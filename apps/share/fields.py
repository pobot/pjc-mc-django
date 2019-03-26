# -*- coding: utf-8 -*-
from django.db import models

__author__ = 'Eric Pascual'


class UpperCasedField(models.CharField):
    description = "A CharField containing an automatically upper cased value"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.upper() if value else value


class LastNameField(UpperCasedField):
    description = "An UpperCasedField with sensible defaults for the last name of somebody"

    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', 'nom')
        max_length = kwargs.pop('max_length', 30)
        super().__init__(*args, verbose_name=verbose_name, max_length=max_length, **kwargs)


class FirstNameField(models.CharField):
    description = "A CharField containing a capitalized first name"

    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', 'prénom')
        max_length = kwargs.pop('max_length', 30)
        super().__init__(*args, verbose_name=verbose_name, max_length=max_length, **kwargs)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.title() if value else value