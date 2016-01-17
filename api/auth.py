from __future__ import unicode_literals

import datetime
from calendar import timegm
from urllib.parse import parse_qsl

import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from social.apps.django_app.utils import psa

from dss import settings


@psa()
def auth_by_token(request, backend, auth_token):
    """Decorator that creates/authenticates a user with an access_token"""

    user = request.backend.do_auth(
            access_token=auth_token
    )
    if user:
        return user
    else:
        return None


def get_access_token(request, backend):
    """
    Tries to get the access token from an OAuth Provider
    :param request:
    :param backend:
    :return:
    """
    access_token_url = ''
    secret = ''

    if backend == 'facebook':
        access_token_url = 'https://graph.facebook.com/oauth/access_token'
        secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
    if backend == 'twitter':
        access_token_url = 'https://api.twitter.com/oauth/request_token'
        secret = settings.SOCIAL_AUTH_TWITTER_SECRET

    params = {
        'client_id': request.data.get('clientId'),
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


class SocialLoginHandler(APIView):
    """View to authenticate users through social media."""
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        backend = request.query_params.get(u'backend', None)
        auth_token = get_access_token(request, backend)
        if auth_token and backend:
            try:
                # Try to authenticate the user using python-social-auth
                user = auth_by_token(request, backend, auth_token)
            except Exception:
                return Response({'status': 'Bad request',
                                 'message': 'Could not authenticate with the provided token.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if user:
                if not user.is_active:
                    return Response({'status': 'Unauthorized',
                                     'message': 'The user account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)

                # This is the part that differs from the normal python-social-auth implementation.
                # Return the JWT instead.

                # Get the JWT payload for the user.
                payload = jwt_payload_handler(user)

                # Include original issued at time for a brand new token,
                # to allow token refresh
                if api_settings.JWT_ALLOW_REFRESH:
                    payload['orig_iat'] = timegm(
                            datetime.datetime.utcnow().utctimetuple()
                    )

                # Create the response object with the JWT payload.
                response_data = {
                    'token': jwt_encode_handler(payload)
                }

                return Response(response_data)
        else:
            return Response({'status': 'Bad request',
                             'message': 'Authentication could not be performed with received data.'},
                            status=status.HTTP_400_BAD_REQUEST)


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
