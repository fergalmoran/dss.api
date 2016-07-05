from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from spa.models import UserProfile


def favourites(request, uid):
    try:
        user = UserProfile.objects.order_by('-id').get(uid=uid)
    except UserProfile.DoesNotExist:
        raise Http404("User does not exist")

    fav_list = user.favourites.all()
    return _render_podcast(request, user, fav_list)


def _render_podcast(request, user, list):
    context = {
        'title': 'DSS Favourites',
        'description': 'All your favourites on Deep South Sounds',
        'link': 'https://deepsouthsounds.com/',
        'user': user.first_name,
        'summary': 'Deep South Sounds is a collective of like minded house heads from Ireland&quot;s Deep South',
        'last_build_date': list[0].upload_date,
        'objects': list,
    }
    response = render_to_response(
        'podcast/feed.xml',
        context=context,
        context_instance=RequestContext(request),
        content_type='application/rss+xml'
    )
    return response
