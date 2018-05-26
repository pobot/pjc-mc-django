# -*- coding: utf-8 -*-

import logging

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import ModelForm, ChoiceField, HiddenInput
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView, ContextMixin

import match.models
from teams.models import Team
from event.views.commons import AppMixin

__author__ = 'Eric Pascual'

logger = logging.getLogger('pjc.' + __name__)
logger.setLevel(logging.INFO)


class MatchMixin(ContextMixin):
    """ This mixin injects the appropriate title based on the involved match"""
    match_num = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Epreuve %s' % self.match_num,
        })
        return context


class LoginForm(AuthenticationForm):
    """ Customized login form with selection of the user via a combo initialized with referees only """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'] = ChoiceField(
            choices=(
                (user.username, user.username)
                for user in User.objects.filter(groups__name__icontains='arbitre').order_by('username')
            )
        )


class HomeView(TemplateView, AppMixin):
    template_name = "refereeing/home.html"
    login_url = reverse_lazy("refereeing:login")


class RoboticsBaseView(LoginRequiredMixin, CreateView, AppMixin, MatchMixin):
    form_class = None
    template_name = 'refereeing/robotics_form.html'
    success_url = reverse_lazy("refereeing:home")
    login_url = reverse_lazy("refereeing:login")

    match_num = None
    # set this to True and implement get_random_config if this round uses random configurations
    random_configuration = False
    # by default, the random configuration is supposed to be drawn once, before the match. Change to False if
    # it can be drawn again during the match. In this case, the button will not be hidden after the first use.
    config_only_once = True
    # set this to the field storing the time used by the robot to complete the round if relevant
    used_time_field = None
    # tells if multiple trials are allowed for the match
    multi_trials_allowed = False
    # field reset values
    reset_values = {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.get('initial', {}).update({
            'referee': self.request.user.id
        })
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Résultats enregistrés.')
        logger.info('résultats match {match} équipe {team.num} ({team.name}) enregistrés par {referee}'.format(
            match=self.match_num,
            team=form.instance.team,
            referee=self.request.user.username
        ))
        return response

    def get_context_data(self, **kwargs):
        kwargs.update({
            'match_num': self.match_num,
            'random_config': self.random_configuration,
            'config_only_once': 'config_only_once' if self.config_only_once else '',
            'used_time_field': self.used_time_field or '',
            'multi_trials_allowed': self.multi_trials_allowed,
            'reset_values': self.reset_values,
        })
        return super().get_context_data(**kwargs)

    @classmethod
    def get_random_config(cls):
        raise NotImplementedError()


def robotics_form_class(match_num):
    class Form(ModelForm):
        class Meta:
            model = getattr(match.models, 'Robotics%d' % match_num)
            widgets = {
                'referee': HiddenInput(),
                "used_time": HiddenInput(),
            }
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # propose only teams who have not already participated to this round
            self.fields['team'].queryset = Team.objects.filter(**{'robotics%d__isnull' % match_num: True})

    return Form


def get_random_configuration(request, match_num):
    """ Request handler returning a random terrain configuration for matches 
    requiring it.

    It delegates the real computation to the view `get_random_config()` method
    if the view declares supporting it by having its `random_configuration` class
    attribute set to True.
    """
    from refereeing.views.edition import Robotics1CreateView, Robotics2CreateView, Robotics3CreateView
    rob_views = [Robotics1CreateView, Robotics2CreateView, Robotics3CreateView]

    view = rob_views[int(match_num) - 1]
    if view.random_configuration:
        return HttpResponse(view.get_random_config())
    else:
        return HttpResponse(status=418)  # let's joke :)
