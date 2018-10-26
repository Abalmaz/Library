#!/bin/sh

sleep 10
./manage.py migrate
./load_db.sh
./manage.py rebuild_index --noinput
gunicorn --workers 3 --bind :8000 library.wsgi:application
