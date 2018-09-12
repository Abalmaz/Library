# Library_django
## Start project

1. Install requremints:
  pip install -r requirements.txt
2. Create DB:
  * python manage.py migrate
3. Load data to DB:
  * python manage.py loaddata country.json
  * python manage.py loaddata genre.json
  * python manage.py loaddata PublishingHouse.json
  * python manage.py loaddata author.json
  * python manage.py loaddata book.json
  * python manage.py loaddata m2m.json
