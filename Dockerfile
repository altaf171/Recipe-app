FROM python:3.8-bullseye

LABEL org.opencontainers.image.authors="ALTAF HUSEN"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install postgresql-client -y
RUN apt-get autoclean && apt-get autoremove 
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app


RUN adduser --disabled-login user
USER user
