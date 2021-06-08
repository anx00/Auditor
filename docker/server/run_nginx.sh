#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
nginx
gunicorn -b 0.0.0.0:1000 --workers=2 --threads=4 --worker-class=gthread APIServer.wsgi
