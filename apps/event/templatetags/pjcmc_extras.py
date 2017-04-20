# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

from pjc_mc import version

__author__ = 'Eric Pascual'

register = template.Library()


@register.simple_tag()
def app_version():
    return version


@register.simple_tag()
def pjc_edition():
    return settings.PJC['edition']


@register.simple_tag()
def edition_thema():
    return settings.PJC['thema']
