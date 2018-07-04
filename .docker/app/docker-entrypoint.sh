#!/usr/bin/env bash
set -e
echo "PWD=$PWD"

DJANGO_SETTINGS_MODULE=django_project.settings_build python3 django_project/manage.py collectstatic --noinput \
    > logs/collectstatic.log 2>&1 || (cat logs/collectstatic.log && false)


python3 django_project/manage.py migrate
DEVEL=1 talisker --reload --bind=0.0.0.0:9000 --workers=2 django_project.wsgi:application

# development mode
#python django_project/manage.py runserver 0.0.0.0:9000
