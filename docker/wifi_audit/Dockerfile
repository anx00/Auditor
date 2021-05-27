# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
apt-get install -y rabbitmq-server net-tools wireless-tools nmap network-manager cron

# Copia los ficheros 'requirements.txt', 'run.sh' y el contenido de 'app/' en el directorio '/app/' dentro del contenedor.
COPY requirements.txt run.sh app/ /app/

# El directorio desde donde se ejecutarán comandos dentro del contenedor.
WORKDIR /app

# Instala movidas
RUN chmod +rx run.sh && \
pip install -r requirements.txt

EXPOSE 8000

# Este comando es el que se va a ejecutar cuando levantas el contenedor.
CMD ["./run.sh"]
