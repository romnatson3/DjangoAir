#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic --no-input --clear
gunicorn main.wsgi:application --workers=1 --log-level=info --bind 0.0.0.0:8000
