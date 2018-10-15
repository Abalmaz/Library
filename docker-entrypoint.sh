#!/bin/sh

./manage.py migrate
./load_db.sh
gunicorn --workers 3 --bind :8000 library.wsgi:application
