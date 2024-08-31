FROM python:3.7

RUN apt-get update && apt-get install -y python-dev libsasl2-dev libssl-dev

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /code/
