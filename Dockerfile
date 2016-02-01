FROM fergalmoran/django

RUN mkdir /code
RUN mkdir /srv/logs
RUN mkdir /files
RUN mkdir /files/static
RUN mkdir /files/media
RUN mkdir /files/cache
RUN mkdir /files/cache/mixes
RUN mkdir /files/cache/waveforms
RUN mkdir /files/tmp
RUN touch /files/tmp/dss.log

WORKDIR /code

ADD requirements.txt /code/
ADD . /code/


RUN npm install -g yuglify
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' djworker
RUN chown djworker /files -R
