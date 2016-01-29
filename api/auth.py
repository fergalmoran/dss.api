import datetime
import json
from calendar import timegm
from urllib.parse import parse_qsl

import requests
from allauth.socialaccount import models as aamodels
from requests_oauthlib import OAuth1
from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from dss import settings
from spa.models import UserProfile
from spa.models.socialaccountlink import SocialAccountLink


def _temp_reverse_user(uid, provider, access_token, access_token_secret, payload):
    """
        Do some magic here to find user account and deprecate psa
        1. Look for account in
    """
    user = None
    try:
        sa = SocialAccountLink.objects.get(social_id=uid)
        sa.type = provider
        sa.social_id = uid
        sa.access_token = access_token
        sa.access_token_secret = access_token_secret
        sa.provider_data = payload
        sa.save()
        user = UserProfile.objects.get(id=sa.user.id)
    except SocialAccountLink.DoesNotExist:
        # try allauth
        try:
            aa = aamodels.SocialAccount.objects.get(uid=uid)
            try:
                user = UserProfile.objects.get(user__id=aa.user_id)
            except UserProfile.DoesNotExist:
                print('Need to create UserProfile')
            # we got an allauth, create the SocialAccountLink
            sa = SocialAccountLink()
            sa.user = user
            sa.social_id = aa.uid
            sa.type = aa.provider
            sa.access_token = access_token
            sa.access_token_secret = access_token_secret
            sa.provider_data = payload
            sa.save()
        except aamodels.SocialAccount.DoesNotExist:
            print('Need to create social model')

    return user if user else None


class SocialLoginHandler(APIView):
    """View to authenticate users through social media."""
    permission_classes = (AllowAny,)

    def post(self, request):
        uid = None
        backend = request.query_params.get('backend')
        user = None
        if backend in ['twitter']:
            request_token_url = 'https://api.twitter.com/oauth/request_token'
            access_token_url = 'https://api.twitter.com/oauth/access_token'
            access_token = ""
            access_token_secret = ""
            if request.data.get('oauth_token') and request.data.get('oauth_verifier'):
                auth = OAuth1(settings.SOCIAL_AUTH_TWITTER_KEY,
                              client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              resource_owner_key=request.data.get('oauth_token'),
                              verifier=request.data.get('oauth_verifier'))
                r = requests.post(access_token_url, auth=auth)
                profile = dict(parse_qsl(r.text))
                payload = json.dumps(profile)
                uid = profile.get('user_id')
                access_token = profile.get('oauth_token')
                access_token_secret = profile.get('oauth_token_secret')
                user = _temp_reverse_user(uid, 'twitter', access_token, access_token_secret, payload)
            else:
                oauth = OAuth1(settings.SOCIAL_AUTH_TWITTER_KEY,
                               client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                               callback_uri=settings.TWITTER_CALLBACK_URL)
                r = requests.post(request_token_url, auth=oauth)
                access_token = dict(parse_qsl(r.text))
                return Response(access_token)

        elif backend in ['facebook']:
            access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
            graph_api_url = 'https://graph.facebook.com/v2.3/me'
            access_token = ""
            access_token_secret = ""
            params = {
                'client_id': request.data.get('clientId'),
                'redirect_uri': request.data.get('redirectUri'),
                'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                'code': request.data.get('code')
            }

            # Step 1. Exchange authorization code for access token.
            r = requests.get(access_token_url, params=params)
            token = json.loads(r.text)

            # Step 2. Retrieve information about the current user.
            r = requests.get(graph_api_url, params=token)
            profile = json.loads(r.text)
            access_token = token.get('access_token')
            uid = profile.get('id')
            user = _temp_reverse_user(uid, 'facebook', access_token, access_token_secret, r.text)
        elif backend in ['google']:
            access_token_url = 'https://accounts.google.com/o/oauth2/token'
            people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
            access_token = ""
            access_token_secret = ""
            payload = dict(client_id=request.data.get('clientId'),
                           redirect_uri=request.data.get('redirectUri'),
                           client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH_SECRET,
                           code=request.data.get('code'),
                           grant_type='authorization_code')

            # Step 1. Exchange authorization code for access token.
            r = requests.post(access_token_url, data=payload)
            token = json.loads(r.text)
            headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

            # Step 2. Retrieve information about the current user.
            r = requests.get(people_api_url, headers=headers)
            profile = json.loads(r.text)
            uid = profile.get('sub')
            user = _temp_reverse_user(uid, 'google', access_token, access_token_secret, r.text)

        if uid is not None and user is not None:
            if not user.user.is_active:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'User account disabled'
                }, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt_payload_handler(user.user)
            if api_settings.JWT_ALLOW_REFRESH:
                payload['orig_iat'] = timegm(
                    datetime.datetime.utcnow().utctimetuple()
                )

            response_data = {
                'token': jwt_encode_handler(payload),
                'session': user.get_session_id()
            }

            return Response(response_data)

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
