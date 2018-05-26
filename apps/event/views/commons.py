# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.base import ContextMixin

from pjc_mc import version

__author__ = 'Eric Pascual'


class AppMixin(ContextMixin):
    """ This mixin injects application wide data, such the title and the version """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'brand': settings.PJC['title_long'],
            'version': version,
        })
        return context


