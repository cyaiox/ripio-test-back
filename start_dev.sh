#!/bin/bash

source ../env/bin/activate

pkill -f celery
pkill -f manage.py

celery -A altcoin worker -B -l info &

python manage.py runserver &
