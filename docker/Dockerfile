FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /alphavantage_app/backend
COPY ./backend /alphavantage_app/backend
COPY ./main.py /alphavantage_app/main.py

RUN pip3 install --upgrade pip
RUN pip3 install -r /alphavantage_app/backend/requirements.txt

WORKDIR /alphavantage_app