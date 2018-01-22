FROM fergalmoran/django

ADD . /code/

RUN mkdir /files/static
RUN mkdir /files/media
RUN mkdir /files/cache/mixes
RUN mkdir /files/cache/waveforms
RUN touch /files/tmp/dss.log
RUN chmod 777 /files/tmp/dss.log
RUN chmod 777 /files/cache -R

RUN chmod +x /code/bin/wav2png
RUN chmod +x /code/run_web.sh
RUN chmod +x /code/run_celery.sh

WORKDIR /code
RUN pip install -r requirements.txt
