FROM fergalmoran/django

ADD . /code/

RUN mkdir /files/static && \
    mkdir /files/media && \
    mkdir /files/cache/mixes && \
    mkdir /files/cache/waveforms && \
    touch /files/tmp/dss.log && \
    chmod 777 /files/tmp/dss.log && \
    chmod 777 /files/cache -R && \
    chmod +x /code/bin/wav2png && \
    chmod +x /code/run_web.sh && \
    chmod +x /code/run_celery.sh

WORKDIR /code
#RUN pip install -r requirements.txt
