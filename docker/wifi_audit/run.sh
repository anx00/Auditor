#!/bin/sh


service cron start
celery -A wifi_audit worker -l info &
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python manage.py makemigrations
python manage.py migrate
python manage.py crontab add
python manage.py runserver 0.0.0.0:8000 -v 3
