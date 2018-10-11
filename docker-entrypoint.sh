#!/bin/sh

./manage.py migrate
./load_db.sh
./manage.py runserver 0.0.0.0:8000
exec "$@"
