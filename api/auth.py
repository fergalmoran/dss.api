from calendar import timegm
import datetime
import logging
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

logger = logging.getLogger('spa')


@psa()
def auth_by_token(request, backend):
    user = request.backend.do_auth(
        access_token=request.data.get('access_token')
    )

    return user if user else None


class SocialLoginHandler(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        auth_token = request.data.get('access_token', None)
        backend = request.data.get('backend', None)

        if auth_token and backend:
            try:
                user = auth_by_token(request, backend)
            except Exception, e:
                logger.exception(e)
                return Response({
                    'status': 'Bad request',
                    'message': e.message
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
