"""
Django settings for pjc_mc_django project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

from django.conf.locale.fr import formats as fr_formats
from django.conf import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print('BASE_DIR =', BASE_DIR)

# add the apps grouping folder to the path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# This is not to kept like this in a production application exposed on the Internet,
# but we don't care here
SECRET_KEY = 'rx6@n_*89)$be-ghi)jo=lud62t9005c-4b^mt+a-1^l!sek$i'
DEBUG = True
# print('DEBUG =', DEBUG)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'bootstrap3',
    'solo',
    # application
    'teams.config.TeamsAppConfig',
    'match.config.MatchAppConfig',
    'research.config.ResearchAppConfig',
    'event.config.EventAppConfig',
    'display.config.DisplayAppConfig',
    'refereeing.config.RefereeingAppConfig',
    'docmaker.config.DocMakerAppConfig',
    'spip.config.SpipAppConfig',
    'volunteers.config.VolunteersAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pjc_mc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pjc_mc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

fr_formats.TIME_FORMAT = "H:i"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# print('STATICFILES_DIRS =', STATICFILES_DIRS)

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

SESSION_COOKIE_AGE = 60 * 60        # in minutes
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

try:
    ADMIN_EMAIL = os.environ['PJCMC_ADMIN_EMAIL']
except KeyError as e:
    raise ImproperlyConfigured('Environment variable not set : %s' % e)
