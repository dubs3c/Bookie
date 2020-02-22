#!/bin/bash

set -eoux pipefail

if [ "$1" == 'prod' ]; then
    echo "Run migrate"
    python manage.py migrate --settings=bookie.env.prod
    echo "Run collectstatic"
    python manage.py collectstatic --noinput --settings=bookie.env.prod
    echo "le go"
    ~/.local/bin/gunicorn bookie.wsgi --env DJANGO_SETTINGS_MODULE=bookie.env.prod --config=gunicorn.config.py
elif [ "$1" == 'dev' ]; then
    echo "Run Migrations"
    python manage.py makemigrations --settings=bookie.env.dev
    python manage.py migrate --settings=bookie.env.dev
    python manage.py runserver 0.0.0.0:8000 --settings=bookie.env.dev
elif [ "$1" == 'manage' ]; then
    shift
    echo "Manage.py $@"
    python manage.py $@
else
    exec "$@"
fi