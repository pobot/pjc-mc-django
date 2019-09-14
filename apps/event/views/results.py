# -*- coding: utf-8 -*-

import logging

from django.forms import ChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from event.views.commons import AppMixin
from event.models import Ranking, RankingType

__author__ = 'Eric Pascual'

__all__ = [
    'LoginForm',
    'HomeView',
    'ResultsLegoView', 'ResultsArduinoView', 'ResultsRPiView',
    'BestRobotView', 'BestLegoView', 'BestArduinoView', 'BestRPiView',
    'BestResearchView', 'BestPosterView'
]

logger = logging.getLogger('pjc.' + __name__)
logger.setLevel(logging.INFO)


class LoginForm(AuthenticationForm):
    """ Customized login form with selection of the user via a combo initialized with staff users only """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'] = ChoiceField(
            choices=(
                (user.username, user.username)
                for user in User.objects.filter(is_staff=True).order_by('username')
            )
        )


class EventView(LoginRequiredMixin, AppMixin):
    login_url = reverse_lazy("event:login")


class HomeView(EventView, TemplateView):
    template_name = "event/home.html"


class ResultsView(EventView, TemplateView):
    template_name = "event/results.html"
    title = 'Classement %s'
    result_type = None
    category = None
    order_by = '-general'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title % self.result_type,
            'ranking': self.get_ranking(),
        })
        return context

    def get_queryset(self):
        return Ranking.objects.filter(type_code=self.category.value).order_by(self.order_by)

    def get_ranking(self):
        raise NotImplementedError()


class GeneralResultsView(ResultsView):
    def get_ranking(self):
        return [
            {
                'rank': result.general,
                'team': result.team.name
            } for result in self.get_queryset()
        ]


class ResultsLegoView(GeneralResultsView):
    result_type = ' Général Mindstorms'
    category = RankingType.Mindstorms


class ResultsArduinoView(GeneralResultsView):
    result_type = 'Général Arduino'
    category = RankingType.Arduino


class ResultsRPiView(GeneralResultsView):
    result_type = 'Général RaspberryPi'
    category = RankingType.RaspberryPi


class BestView(ResultsView):
    title = "Meilleur %s"
    category = None
    criterion = None

    def get_ranking(self):
        return [
            {
                'rank': getattr(result, self.criterion),
                'team': result.team.name,
                'category': result.team.category.name if self.category == RankingType.Scratch else None,
            } for result in self.get_queryset()
        ]

    def get_queryset(self):
        return Ranking.objects.filter(type_code=self.category.value).order_by(self.criterion)[:1]


class BestRobotView(BestView):
    result_type = 'Robot (scratch)'
    category = RankingType.Scratch
    criterion = 'robotics'


class BestLegoView(BestView):
    result_type = 'Robot Mindstorms'
    category = RankingType.Mindstorms
    criterion = 'robotics'


class BestArduinoView(BestView):
    result_type = 'Robot Arduino'
    category = RankingType.Arduino
    criterion = 'robotics'


class BestRPiView(BestView):
    result_type = 'Robot RaspberryPi'
    category = RankingType.RaspberryPi
    criterion = 'robotics'


class BestResearchView(BestView):
    result_type = 'Dossier de Recherche'
    category = RankingType.Scratch
    criterion = 'research'


class BestPosterView(BestView):
    result_type = 'Poster'
    category = RankingType.Scratch
    criterion = 'poster'
