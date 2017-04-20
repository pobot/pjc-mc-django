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
        'template_name': 'refereeing/login.html',
        'extra_context': {
            'brand': settings.PJC['brand']
        }
    }, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': reverse_lazy('refereeing:home')}, name='logout'),
    url(r'^rob1$', Robotics1CreateView.as_view(), name='rob1'),
    url(r'^rob2$', Robotics2CreateView.as_view(), name='rob2'),
    url(r'^rob3$', Robotics3CreateView.as_view(), name='rob3'),
    url(r'^rndcfg/(?P<match_num>[1-3])', get_random_configuration, name='rnd_config'),
]
