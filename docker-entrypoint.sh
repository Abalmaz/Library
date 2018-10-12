#!/bin/sh

./manage.py migrate
./load_db.sh
gunicorn --workers 3 --bind unix:/app/library.sock library.wsgi:application
