FROM fergalmoran/django

ADD . /code/


RUN mkdir /files/static
RUN mkdir /files/media
RUN mkdir /files/cache/mixes
RUN mkdir /files/cache/waveforms
RUN touch /files/tmp/dss.log

WORKDIR /code
