#!/bin/sh
./manage.py loaddata country.json
./manage.py loaddata genre.json
./manage.py loaddata PublishingHouse.json
./manage.py loaddata author.json
./manage.py loaddata book.json
./manage.py loaddata m2m.json
./manage.py loaddata allauth_fixture.json

