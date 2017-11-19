# -*- coding: utf-8 -*-
import random

from .generic import RoboticsBaseView, robotics_form_class

__author__ = 'Eric Pascual'


class Robotics1CreateView(RoboticsBaseView):
    match_num = 1
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True


class Robotics2CreateView(RoboticsBaseView):
    match_num = 2
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True


class Robotics3CreateView(RoboticsBaseView):
    match_num = 3
    form_class = robotics_form_class(match_num)
    multi_trials_allowed = True

    # change it to False if obstacle robot is used
    random_configuration = True

    @classmethod
    def get_random_config(cls):
        return random.choice(['obstacle', 'voie libre'])
