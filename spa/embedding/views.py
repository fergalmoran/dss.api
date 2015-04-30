from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from spa.models import Mix


def mix(request, **args):
    try:
        if 'mix_id' in args:
            mix = Mix.objects.get(pk=args['mix_id'])
        else:
            mix = Mix.objects.get(slug=args['slug'])
    except Mix.DoesNotExist:
        raise Http404

    image = mix.get_image_url('1500x1500')
    audio_url = mix.get_stream_url()
    mix_url = mix.get_absolute_url()
    payload = {
        "description": mix.description.replace('<br />', '\n'),
        "title": mix.title,
        "image_url": image,
        "audio_url": audio_url,
        "mix_url": 'http://%s%s' % (Site.objects.get_current().domain, mix_url)
    }
    response = render_to_response(
        'inc/embed/mix.html',
        payload,
        context_instance=RequestContext(request)
    )
    response['X-XSS-Protection'] = 0
    response['X-Frame-Options'] = 'IGNORE'
    return response
