from celery.task import task
import os
import logging
import json
import requests
from core.realtime import activity
from core.utils import cdn
from spa.models import Mix
from spa.signals import waveform_generated_signal

try:
    from django.contrib.gis.geoip import GeoIP
except ImportError:
    pass

from core.utils.waveform import generate_waveform
from dss import settings

logger = logging.getLogger('dss')


@task(time_limit=3600)
def send_db_signals(uid):
    waveform_generated_signal.send(sender=None, uid=uid)


@task(time_limit=3600)
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.CACHE_ROOT, 'waveforms/%s.png' % uid)
    logger.info("Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file))
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        logger.info("Waveform generated successfully")
        return out_file
    else:
        logger.error("Outfile is missing")


@task(time_limit=3600)
def update_file_http_headers(uid, title):
    cdn.set_azure_details(
        blob_name='{0}.mp3'.format(uid),
        download_name='Deep South Sounds - {0}.mp3'.format(title),
        container_name='mixes')


@task(time_limit=3600)
def upload_to_cdn_task(filetype, uid, container_name):
    source_file = os.path.join(settings.CACHE_ROOT, '{0}/{1}.{2}'.format(container_name, uid, filetype))
    try:
        file_name = "{0}.{1}".format(uid, filetype)
        logger.info("Sending {0} to azure".format(source_file))
        print(source_file)
        cdn.upload_file_to_azure(source_file, file_name, container_name)
        logger.info("Sent {0} to azure".format(source_file))
        return source_file
    except Exception as ex:
        logger.error("Unable to upload: {0}".format(ex))


@task
def update_geo_info_task(ip_address, profile_id):
    try:
        ip = '188.141.70.110' if ip_address == '127.0.0.1' else ip_address
        if ip:
            g = GeoIP()
            city = g.city(ip)
            country = g.country(ip)
            print("Updated user location")
    except Exception as e:
        logger.exception(e)
        pass


@task
def notify_subscriber(session_id, uid):
    if session_id is not None:
        message = {'type': 'waveform', 'target': uid}
        logger.info("Tasks: notifying user:process. Session: {} Message: {}".format(session_id, message))
        activity.post_activity('user:process', message=message, session=session_id)


@task
def play_pending_audio():
    m = Mix.objects.order_by('?').first()
    print("Playing: {}".format(m.title))

    data = {'audio_file': m.get_stream_url()}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post('http://localhost:8888/a/play', data=json.dumps(data), headers=headers)
    print(r.text)
