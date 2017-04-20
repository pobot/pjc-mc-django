# -*- coding: utf-8 -*-

from django import template

from teams.models import Team

__author__ = 'Eric Pascual'

register = template.Library()


@register.filter()
def disabled_round(num):
    return "" if num != 1 else "disabled"
    # return "" if Team.objects.filter(**{'robotics%d__isnull' % num: True}).exists() else "disabled"


@register.filter()
def round_status(num):
    return "" if num != 1 else "(complète)"
    # return "" if Team.objects.filter(**{'robotics%d__isnull' % num: True}).exists() else "(complète)"


@register.filter()
def round_menu_class(num):
    class_attr = disabled_round(num)
    # don't put quotes around the value since already here because the function has been wrapped as a filter
    return ('class=%s' % class_attr) if class_attr else ""
