#!/usr/bin/env bash

PYTHONPATH=. gunicorn --config gunicorn/config.py pjc_mc.wsgi
