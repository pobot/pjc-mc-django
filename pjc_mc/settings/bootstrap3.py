# -*- coding: utf-8 -*-

from django.conf import settings

__all__ = ['BOOTSTRAP3']


def _static(path):
    return settings.STATIC_URL + path.lstrip('/')


BOOTSTRAP3 = {
    'jquery_url': _static('js/jquery.min.js'),
    'css_url': _static('css/bootstrap.min.css'),
    'javascript_url': _static('js/bootstrap.min.js'),
}
