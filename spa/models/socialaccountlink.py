import json
import logging
import urllib.error
import urllib.parse
import urllib.request

import facebook
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from requests_oauthlib import OAuth1Session

from dss import settings
from spa.models import BaseModel
from spa.models.userprofile import UserProfile

logger = logging.getLogger(__name__)

class SocialAccountLink(BaseModel):
    ACCOUNT_TYPE = (
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('google', 'Google')
    )
    type = models.CharField(max_length=30, choices=ACCOUNT_TYPE)
    social_id = models.CharField(max_length=150)
    user = models.ForeignKey(UserProfile, related_name='social_accounts', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    access_token_secret = models.CharField(max_length=500, null=True, blank=True)
    provider_data = models.CharField(max_length=2000, null=True, blank=True)

    def _save_image(self, url):

        img = NamedTemporaryFile(delete=True)
        img.write(urllib.request.urlopen(url).read())

        img.flush()
        self.user.avatar_image.save(str(self.user.id), File(img))

    def update_image_url(self):
        try:
            if self.type in ['twitter']:
                twitter = OAuth1Session(
                    settings.SOCIAL_AUTH_TWITTER_KEY,
                    client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                    resource_owner_key=self.access_token,
                    resource_owner_secret=self.access_token_secret)
                url = 'https://api.twitter.com/1.1/users/show.json?user_id={0}'.format(self.social_id)
                response = twitter.get(url)
                r = json.loads(response.text)
                self._save_image(r.get('profile_image_url'))
            elif self.type in ['facebook']:
                graph = facebook.GraphAPI(access_token=self.access_token, version=settings.FACEBOOK_API_VERSION)
                image_url = graph.get_object("me/picture?type=large")
                self._save_image(image_url.get('url'))
            elif self.type in ['google']:
                data = json.loads(self.provider_data)
                self._save_image(data.get('picture'))
        except Exception as ex:
            logger.exception(ex)
