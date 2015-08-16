from celery.task import task
import os
import logging
from core.realtime import activity

from core.utils import cdn
from spa.signals import waveform_generated_signal

try:
    from django.contrib.gis.geoip import GeoIP
except ImportError:
    pass

from core.utils.waveform import generate_waveform
from dss import settings

logger = logging.getLogger('dss')


@task(time_limit=3600)
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.CACHE_ROOT, 'waveforms/%s.png' % uid)
    logger.info("Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file))
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        logger.info("Waveform generated successfully")
        waveform_generated_signal.send(sender=None, uid=uid, path=in_file)
        return out_file
    else:
        logger.error("Outfile is missing")


@task(timse_limit=3600)
def upload_to_cdn_task(filetype, uid, container_name):
    source_file = os.path.join(settings.CACHE_ROOT, '{0}/{1}.{2}'.format(container_name, uid, filetype))
    logger.info("Sending {0} to azure".format(uid))
    try:
        file_name = "{0}.{1}".format(uid, filetype)
        cdn.upload_file_to_azure(source_file, file_name, container_name)
        return source_file
    except Exception, ex:
        logger.error("Unable to upload: {0}".format(ex.message))


@task
def update_geo_info_task(ip_address, profile_id):
    try:
        ip = '188.141.70.110' if ip_address == '127.0.0.1' else ip_address
        if ip:
            g = GeoIP()
            city = g.city(ip)
            country = g.country(ip)
            print "Updated user location"
    except Exception, e:
        logger.exception(e)
        pass


@task
def notify_subscriber(session_id, uid):
    if session_id is not None:
        activity.post_activity('user:process', session_id, {'type': 'waveform', 'target': uid})
