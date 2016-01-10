from calendar import timegm

import datetime
import logging

import requests
from requests_oauthlib import OAuth1
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework import parsers

from social.apps.django_app.utils import psa
from urllib.parse import parse_qsl

from dss import settings

logger = logging.getLogger('dss')

BACKENDS = {
    'google': 'google-oauth2',
    'facebook': 'facebook',
    'twitter': 'twitter'
}


@psa()
def auth_by_token(request, backend, auth_token):
    user = request.backend.do_auth(
            access_token=auth_token
    )

    return user if user else None


def get_access_token(request, backend):
    """
    Tries to get the access token from an OAuth Provider
    :param request:
    :param backend:
    :return:
    """
    access_token_url = ''
    secret = ''

    client_id = None
    if backend == 'facebook':
        access_token_url = 'https://graph.facebook.com/oauth/access_token'
        secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        params = {
            'client_id': client_id or request.data.get('clientId'),
            'redirect_uri': request.data.get('redirectUri'),
            'client_secret': secret,
            'code': request.data.get('code')
        }

        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        try:
            access_token = dict(parse_qsl(r.text))['access_token']
        except KeyError:
            access_token = 'FAILED'
        return access_token

    elif backend == 'twitter':
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'

        if request.data.get('oauth_token') and request.data.get('oauth_verifier'):
            auth = OAuth1(settings.SOCIAL_AUTH_TWITTER_KEY,
                          settings.SOCIAL_AUTH_TWITTER_SECRET,
                          resource_owner_key=request.data.get('oauth_token'),
                          verifier=request.data.get('oauth_verifier'))
            r = requests.post(access_token_url, auth=auth)
            profile = dict(parse_qsl(r.text))
        else:
            oauth = OAuth1(settings.SOCIAL_AUTH_TWITTER_KEY,
                           client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                           callback_uri='http://ext-test.deepsouthsounds.com:9000/')
            r = requests.post(request_token_url, auth=oauth)
            oauth_token = dict(parse_qsl(r.text))
            return oauth_token.get('oauth_token_secret')


class SocialLoginHandler(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        backend = request.query_params.get('backend', None)
        auth_token = get_access_token(request, backend)

        if auth_token and backend:
            try:
                user = auth_by_token(request, backend, auth_token)
            except Exception as e:
                logger.exception(e)
                return Response({
                    'status': 'Bad request',
                    'message': e
                }, status=status.HTTP_400_BAD_REQUEST)

            if user:
                if not user.is_active:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'User account disabled'
                    }, status=status.HTTP_401_UNAUTHORIZED)

                payload = jwt_payload_handler(user)
                if api_settings.JWT_ALLOW_REFRESH:
                    payload['orig_iat'] = timegm(
                            datetime.datetime.utcnow().utctimetuple()
                    )

                response_data = {
                    'token': jwt_encode_handler(payload),
                    'session': user.userprofile.get_session_id()
                }

                return Response(response_data)

        else:
            return Response({
                'status': 'Bad request',
                'message': 'Authentication could not be performed with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)


class ObtainUser(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        return self.get(request)

    def get(self, request):
        if request.user.is_authenticated():
            return Response(
                    status=status.HTTP_200_OK, data={
                        'id': request.user.id,
                        'name': request.user.username,
                        'slug': request.user.userprofile.slug,
                        'userRole': 'user'
                    })
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
