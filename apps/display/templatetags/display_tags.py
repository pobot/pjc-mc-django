# -*- coding: utf-8 -*-

import datetime

import arrow

from django import template
from django.utils.safestring import mark_safe


__author__ = 'Eric Pascual'

register = template.Library()

PLANNING_STATUS_CLASSES = ['', 'text-warning', 'text-danger']
PLANNING_LIMIT_CLASSES = ['', 'text-warning', 'text-danger']


@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))


def emergency_level(time):
    now = datetime.datetime.now()
    if isinstance(time, str):
        time = arrow.get(time, "HH:mm")
    t_s, now_s = (_t.hour * 3600 + _t.minute * 60 + _t.second for _t in (time, now))
    dt = (t_s - now_s) / 60
    if dt > 10:
        return 0
    elif dt > 0:
        return 1
    else:
        return 2


@register.filter(name="planning_status_class")
def planning_status_class(when):
    return PLANNING_STATUS_CLASSES[emergency_level(when)]


@register.filter(name="planning_limit_class")
def planning_limit_class(when):
    return PLANNING_LIMIT_CLASSES[emergency_level(when)]


@register.filter(name="emergency_class")
def emergency_class(when):
    now = datetime.datetime.now().time()
    if isinstance(when, str):
        when = arrow.get(when, "HH:mm")
    t_s, now_s = (_t.hour * 3600 + _t.minute * 60 + _t.second for _t in (when, now))
    dt = (t_s - now_s) / 60
    if dt > 10:
        return 'active'
    elif dt > 5:
        return 'warning'
    else:
        return 'danger'


@register.filter(name="verbose_location")
def verbose_location(schedule_detail):
    if schedule_detail['what'] == 'exposé':
        return "jury %s" % schedule_detail['where']
    else:
        return "table %s" % schedule_detail['where']


@register.filter(name="best_class")
def best_class(is_best):
    return ""