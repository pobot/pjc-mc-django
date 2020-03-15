#!/bin/bash
python manage.py migrate                  # Apply database migrations
#python manage.py collectstatic --noinput  # Collect static files


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn pjc_mc.wsgi:application --config /app/gunicorn/config.py "$@"
