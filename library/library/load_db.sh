#!/bin/bash
./manage.py loaddata country.json
./python manage.py loaddata genre.json
./python manage.py loaddata PublishingHouse.json
./python manage.py loaddata author.json
./python manage.py loaddata book.json
./python manage.py loaddata m2m.json
./python manage.py loaddata ratings.json
./python manage.py loaddata user_ratings.json
