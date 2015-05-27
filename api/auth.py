from requests import HTTPError
from rest_framework import parsers
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import renderers
from social.apps.django_app.utils import strategy, load_strategy, load_backend
from dss import settings


class LoginException(Exception):
    pass


@strategy()
def register_by_access_token(request, backend):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'social':
        raise LoginException("Unable to register_by_access_token: No token header provided")

    access_token = auth[1]
    return request.backend.do_auth(access_token)
"""
class RefreshTokenView(APIView):
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        # Here we call PSA to authenticate like we would if we used PSA on server side.
        try:
            backend = request.META.get('HTTP_AUTH_BACKEND')
            if backend is None:
                # Work around django test client oddness
                return Response("No Auth-Backend header specified", HTTP_400_BAD_REQUEST)

            user = refresh_access_token(request, backend)

            # If user is active we get or create the REST token and send it back with user data
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'slug': user.userprofile.slug,
                    'token': token.key
                })
        except LoginException, ex:
            return Response(ex.message, HTTP_400_BAD_REQUEST)
        except HTTPError, ex:
            if ex.response.status_code == 400:
                return Response(ex.message, HTTP_401_UNAUTHORIZED)
            return Response(ex.message, HTTP_400_BAD_REQUEST)
"""

class ObtainAuthToken(APIView):
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        # Here we call PSA to authenticate like we would if we used PSA on server side.
        try:
            backend = request.META.get('HTTP_AUTH_BACKEND')
            if backend is None:
                # Work around django test client oddness
                return Response("No Auth-Backend header specified", HTTP_400_BAD_REQUEST)

            user = register_by_access_token(request, backend)

            # If user is active we get or create the REST token and send it back with user data
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'slug': user.userprofile.slug,
                    'token': token.key
                })
        except LoginException, ex:
            return Response(ex.message, HTTP_400_BAD_REQUEST)
        except HTTPError, ex:
            if ex.response.status_code == 400:
                return Response(ex.message, HTTP_401_UNAUTHORIZED)
            return Response(ex.message, HTTP_400_BAD_REQUEST)


class ObtainUser(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def get(self, request):
        if request.META.get('HTTP_AUTHORIZATION'):

            auth = request.META.get('HTTP_AUTHORIZATION').split()

            if not auth or auth[0].lower() != b'token' or len(auth) != 2:
                msg = 'Invalid token header. No credentials provided.'
                return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

            token = Token.objects.get(key=auth[1])
            if token and token.user.is_active:
                return Response({'id': token.user_id, 'name': token.user.username, 'firstname': token.user.first_name,
                                 'userRole': 'user', 'token': token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ObtainLogout(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    # Logout le user
    def get(self, request):
        return Response({'User': ''})
