#!/usr/bin/env bash

PYTHONPATH=. gunicorn --config gunicorn.conf pjc_mc.wsgi
