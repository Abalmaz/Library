#!/bin/sh
sleep 10
./manage.py migrate
./load_db.sh
./manage.py rebuild_index --noinput
./manage.py runserver 0.0.0.0:8000
exec "$@"
