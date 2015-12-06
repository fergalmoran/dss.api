FROM python:latest
ENV PYTHONBUFFERED 1

RUN mkdir /code
RUN mkdir /srv/logs
RUN mkdir /files
RUN mkdir /files/static
RUN mkdir /files/media
RUN mkdir /files/cache
RUN mkdir /files/cache/mixes
RUN mkdir /files/cache/waveforms
RUN mkdir /files/tmp

WORKDIR /code

ADD requirements.txt /code/
ADD . /code/

RUN apt-get update --fix-missing && apt-get install -y sox lame vim ccze node npm \
    libboost-program-options-dev libsox-fmt-mp3 postgresql-client rsync openssh-client

RUN npm install -g yuglify
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' djworker
RUN chown djworker /files -R
