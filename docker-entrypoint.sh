#!/bin/sh

./manage.py migrate
./load_db.sh
exec "$@"
