FROM python:3.9
RUN apt-get update
RUN apt-get install --assume-yes build-essential nano htop
RUN pip install --upgrade pip

ENV app /transmitata

RUN mkdir $app
WORKDIR $app

ADD . $app
