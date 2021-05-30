FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
apt-get install -y python-django nginx

COPY requirements.txt run_nginx.sh app/ /app/

WORKDIR /app

RUN chmod +rx run_nginx.sh && \
pip install -r requirements.txt && \
pip install gunicorn

COPY app/nginx/nginx.conf /etc/nginx/sites-enabled/app.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

ENTRYPOINT ["./run_nginx.sh"]
