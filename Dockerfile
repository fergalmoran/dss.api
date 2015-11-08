FROM python:3.4.3
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

RUN apt-get update && apt-get install -y sox lame vim \
    libboost-program-options-dev libsox-fmt-mp3 postgresql-client rsync openssh-client

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' djworker
RUN chown djworker /files -R
RUN chown djworker /srv/logs -R
RUN export PATH=$PATH:/mnt/bin/
