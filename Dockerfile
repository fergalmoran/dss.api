FROM fergalmoran/django

ADD . /code/


RUN mkdir /files/
RUN mkdir /files/static
RUN mkdir /files/media
RUN mkdir /files/cache
RUN mkdir /files/cache/mixes
RUN mkdir /files/cache/waveforms
RUN mkdir /files/tmp
RUN touch /files/tmp/dss.log

WORKDIR /code
