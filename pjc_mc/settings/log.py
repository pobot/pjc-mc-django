# -*- coding: utf-8 -*-

from django.utils.log import DEFAULT_LOGGING

__author__ = 'Eric Pascual'

# this is the default, by making it explicit documents things better
LOGGING_CONFIG = 'logging.config.dictConfig'

# use Django default logging conf as a starting point
LOGGING = DEFAULT_LOGGING

# add our stuff
LOGGING['formatters'].update({
    'verbose': {
        'format': '%(asctime)s [%(levelname).1s] %(name)s > %(message)s',
        'datefmt': '%H:%M:%S',
    }
})
LOGGING['handlers'].update({
    'console.pjc': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
})
LOGGING['loggers'].update({
    'pjc': {
        'handlers': ['console.pjc'],
        'level': 'INFO'
    }
})
