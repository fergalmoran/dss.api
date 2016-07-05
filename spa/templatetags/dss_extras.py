from django import template
import datetime
import time
from email import utils

register = template.Library()


@register.filter
def get_mix_url(obj):
    return obj.get_full_url()


@register.filter
def get_mix_audio_url(obj):
    return obj.get_download_url()


@register.filter
def seconds_to_hms(seconds):
    try:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)
    except Exception as ex:
        return "00:00:09"


@register.filter
def date_to_rfc2822(date):
    nowtuple = date.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    return utils.formatdate(nowtimestamp)