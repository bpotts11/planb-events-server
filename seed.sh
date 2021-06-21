#!/bin/bash
rm -rf planbapi/migrations
rm db.sqlite3
python3 manage.py makemigrations planbapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
python3 manage.py loaddata categories
python3 manage.py loaddata vendors
python3 manage.py loaddata tags
python3 manage.py loaddata events
python3 manage.py loaddata products
python3 manage.py loaddata product_tag
python3 manage.py loaddata event_product
python3 manage.py loaddata favorite
python manage.py createsuperuser