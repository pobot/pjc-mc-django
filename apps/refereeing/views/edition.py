# -*- coding: utf-8 -*-
from .generic import RoboticsBaseView, robotics_form_class

__author__ = 'Eric Pascual'


class Robotics1CreateView(RoboticsBaseView):
    match_num = 1
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    reset_values = {
        'sections': 0
    }


class Robotics2CreateView(RoboticsBaseView):
    match_num = 2
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    reset_values = {
        'sections': 0,
        'object_retrieved': False,
    }


class Robotics3CreateView(RoboticsBaseView):
    match_num = 3
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    reset_values = {
        'captured_objects': 0,
        'deposited_objects': 0,
    }
