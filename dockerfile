FROM ubuntu:20.04

WORKDIR /var/www/html

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get upgrade -y
RUN apt-get install -y \
    software-properties-common  && \
    apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libpq-dev \
    build-essential && \
    apt-get -y autoclean && \
    apt-get -y autoremove

RUN python3 -m pip install --upgrade pip

RUN pip3 --version && python3 --version

RUN pip3 install gunicorn psycopg2 PyMySQL[rsa]
