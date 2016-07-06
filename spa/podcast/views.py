from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from spa.models import UserProfile, Mix


def _get_user(uid):
    try:
        user = UserProfile.objects.order_by('-id').get(uid=uid)
    except UserProfile.DoesNotExist:
        raise Http404("User does not exist")
    return user


def featured(request):
    podcast_list = Mix.objects.order_by('-id').filter(is_private=False, is_featured=True)
    return _render_podcast(request, 'Deep South Sounds', 'DSS Favourites',
                           'Featured Deep South Sounds mixes', podcast_list)


def user(request, slug):
    user = UserProfile.objects.get(slug=slug)
    podcast_list = Mix.objects.order_by('-id').filter(is_private=False, user__slug=slug)
    return _render_podcast(request, user.first_name, 'DSS {0}'.format(user.display_name),
                           'All of {0}\'s mixes on Deep South Sounds'.format(user.display_name), podcast_list,
                           image=user.get_sized_avatar_image(1400, 1400))


def favourites(request, uid):
    user = _get_user(uid)
    podcast_list = user.favourites.all()
    return _render_podcast(request, user.first_name, 'DSS Favourites',
                           'All your favourites on Deep South Sounds', podcast_list)


def following(request, uid):
    user = _get_user(uid)
    podcast_list = Mix.objects.order_by('-id').filter(is_private=False, user__in=user.following.all())
    return _render_podcast(request, user.first_name, 'DSS Following',
                           'Mixes from people you follow on Deep South Sounds', podcast_list)


def _render_podcast(request, user, title, description, podcast_list,
                    image='https://dsscdn2.blob.core.windows.net/static/podcast_logo.png'):
    context = {
        'title': title,
        'description': description,
        'link': 'https://deepsouthsounds.com/',
        'image': image,
        'user': user,
        'summary': 'Deep South Sounds is a collective of like minded house heads from Ireland&quot;s Deep South',
        'last_build_date': podcast_list[0].upload_date,
        'objects': podcast_list,
    }
    response = render_to_response(
        'podcast/feed.xml',
        context=context,
        context_instance=RequestContext(request),
        content_type='application/rss+xml'
    )
    return response
