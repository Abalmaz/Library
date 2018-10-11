#!/bin/sh
set -eoux pipefail

if [ "$1" == 'init' ]; then
    echo "Run Migrations"
    ./manage.py migrate
    ./load_db.sh
fi