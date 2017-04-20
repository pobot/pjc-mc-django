# -*- coding: utf-8 -*-
import random

from .generic import RoboticsBaseView, robotics_form_class

__author__ = 'Eric Pascual'


class Robotics1CreateView(RoboticsBaseView):
    match_num = 1
    form_class = robotics_form_class(match_num)


class Robotics2CreateView(RoboticsBaseView):
    match_num = 2
    form_class = robotics_form_class(match_num)
    used_time_field = 'used_time'


class Robotics3CreateView(RoboticsBaseView):
    match_num = 3
    form_class = robotics_form_class(match_num)
    random_configuration = True

    @classmethod
    def get_random_config(cls):
        last_choice = set()
        cfg = []
        for _ in range(3):
            possible = list({1, 2, 3} - last_choice)
            choice = random.choice(possible)
            cfg.append(choice)
            last_choice = {choice}

        return cfg