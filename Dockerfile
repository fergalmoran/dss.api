FROM python:2.7
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
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y sox lame libboost-program-options-dev libsox-fmt-mp3
ADD . /code/

RUN adduser --disabled-password --gecos '' djworker
RUN chown djworker /files -R
RUN chown djworker /srv/logs -R
