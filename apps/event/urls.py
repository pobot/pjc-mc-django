from django.conf import settings
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from .views import *

__author__ = 'Eric Pascual'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login$', auth_views.login, {
        'authentication_form': LoginForm,
        'template_name': 'event/login.html',
        'extra_context': {
            'brand': settings.PJC['brand']
        }
    }, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': reverse_lazy('finals:home')}, name='logout'),
    url(r'^results/lego$', ResultsLegoView.as_view(), name='results_lego'),
    url(r'^results/arduino', ResultsArduinoView.as_view(), name='results_arduino'),
    url(r'^results/rpi', ResultsRPiView.as_view(), name='results_rpi'),

    url(r'^best/robot$', BestRobotView.as_view(), name='best_robot'),
    url(r'^best/lego$', BestLegoView.as_view(), name='best_lego'),
    url(r'^best/arduino', BestArduinoView.as_view(), name='best_arduino'),
    url(r'^best/rpi', BestRPiView.as_view(), name='best_rpi'),
    url(r'^best/research', BestResearchView.as_view(), name='best_research'),
    url(r'^best/poster', BestPosterView.as_view(), name='best_poster'),
]
