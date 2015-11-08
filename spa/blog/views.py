import urllib.request, urllib.error, urllib.parse
import logging

from django.conf.urls import url
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import requests
from allauth.socialaccount.models import SocialToken
from core.utils.url import wrap_full

from dss import settings
from spa.models import Playlist, Blog
from spa.models.mix import Mix
from spa.models.userprofile import UserProfile

logger = logging.getLogger(__name__)

"""
    Handles callbacks from non javascript browsers
"""


def _getPayload(request):
    return {
        "app_id": settings.FACEBOOK_APP_ID,
        "site_url": 'http://%s' % Site.objects.get_current().domain,
        "site_image_url": '%s/img/dss-large.png' % settings.STATIC_URL,
    }


def entry(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
        extras = {
            "content": blog.body,
        }
        payload = dict(list(_getPayload(request).items()) + list(extras.items()))
        response = render_to_response(
            'blog/entry.html',
            payload,
            context_instance=RequestContext(request)
        )
        return response
    except Blog.DoesNotExist:
        raise Http404
    except Exception as ex:
        logger.error(ex)


def index(request):
    response = render_to_response(
        "blog/index.html",
        _getPayload(request),
        context_instance=RequestContext(request))
    return response
