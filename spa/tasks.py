import shutil
from celery.task import task
import os
from core.utils.cdn import upload_to_azure
from spa.signals import waveform_generated_signal

try:
    from django.contrib.gis.geoip import GeoIP
except ImportError:
    pass

from core.utils.waveform import generate_waveform
from dss import settings


@task(time_limit=3600)
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.CACHE_ROOT, 'waveforms/%s.png' % uid)
    print "Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file)
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        print "Waveform generated successfully"
        waveform_generated_signal.send(sender=None, uid=uid)
        return out_file
    else:
        print "Outfile is missing"


@task(timse_limit=3600)
def upload_to_cdn_task(in_file, filetype, uid, container_name):
    source_file = os.path.join(settings.CACHE_ROOT, '{0}/{1}.{2}'.format(container_name, uid, filetype))
    print "Sending {0} to azure".format(uid)
    try:
        upload_to_azure(source_file, filetype, uid, container_name)
        return source_file
    except Exception, ex:
        print "Unable to upload: {0}".format(ex.message)

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
        print e.message
        pass
