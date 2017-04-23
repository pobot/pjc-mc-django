# -*- coding: utf-8 -*-

import logging

from django.conf import settings
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
from pjc_mc import version

__author__ = 'Eric Pascual'

logger = logging.getLogger('pjc.' + __name__)
logger.setLevel(logging.INFO)


class AppMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'brand': settings.PJC['title_long'],
            'version': version,
        })
        return context


class MatchMixin(ContextMixin):
    match_num = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Epreuve %s' % self.match_num,
        })
        return context


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'] = ChoiceField(
            choices=((user.username, user.username)
                     for user in User.objects.filter(groups__name='Arbitres').order_by('username')
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
    # set this to the field storing the time used by the robot to complete the round if relevant
    used_time_field = None

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
            'used_time_field': self.used_time_field or '',
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
        return HttpResponse('-'.join((str(c) for c in view.get_random_config())))
    else:
        return HttpResponse(status=418)  # let's joke :)
