#!/bin/sh

apt-get update && \
apt-get install -y python3 rabbitmq-server net-tools wireless-tools nmap python3.8 python3-pip && \ 
pip install requirements.txt
