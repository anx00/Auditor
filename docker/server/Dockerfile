# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

COPY requirements.txt run.sh app/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["./run.sh"]
