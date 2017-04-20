from django.conf.urls import url

from .views import *

__author__ = 'Eric Pascual'

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^content$', ContentView.as_view()),
]
