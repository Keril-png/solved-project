#!/bin/sh

sleep 2

python3 manage.py migrate
python3 manage.py migrate problems


python3 manage.py collectstatic --noinput
gunicorn solved.wsgi:application --bind 0.0.0.0:8000
ls -la

exec "$@"
