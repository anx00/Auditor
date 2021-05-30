# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
apt-get install -y rabbitmq-server net-tools wireless-tools nmap network-manager cron

COPY requirements.txt run.sh app/ /app/

WORKDIR /app

RUN chmod +rx run.sh && \
pip install -r requirements.txt

EXPOSE 8000

CMD ["./run.sh"]
