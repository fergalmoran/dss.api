from django.core.files.base import ContentFile
from requests import request, ConnectionError


def save_profile(backend, user, response, is_new, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            profile = user.userprofile

            try:
                response = request('GET', url)
                response.raise_for_status()
            except ConnectionError:
                pass
            else:
                profile.avatar_image.save('',
                                          ContentFile(response.content),
                                          save=False)
                profile.save()
    elif backend.name == 'facebook':
        profile = user.userprofile
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except ConnectionError:
            pass
        else:
            profile.avatar_image.save('',
                                      ContentFile(response.content),
                                      save=False
                                      )
            profile.save()
