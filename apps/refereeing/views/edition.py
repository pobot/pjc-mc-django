# -*- coding: utf-8 -*-
from .generic import RoboticsBaseView, robotics_form_class

__author__ = 'Eric Pascual'


class Robotics1CreateView(RoboticsBaseView):
    match_num = 1
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    used_time_field = "used_time"
    input_fields = {
        'travels': 0
    }


class Robotics2CreateView(RoboticsBaseView):
    match_num = 2
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    used_time_field = "used_time"
    input_fields = {
        'travels': 0,
        'moved_obstacles': 0,
    }


class Robotics3CreateView(RoboticsBaseView):
    match_num = 3
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True
    used_time_field = "used_time"
    input_fields = {
        'good_fruits': 0,
        'bad_fruits': 0,
    }
