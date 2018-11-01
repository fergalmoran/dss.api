import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from core import realtime
from core.radio import ice_scrobbler
from core.realtime import activity
from dss import settings
from spa.models import Mix, UserProfile
from core.utils import session


class Helper(APIView):
    pass


class ActivityHelper(APIView):
    def get_session(self, request):
        sessions = session.get_active_sessions(request.session)

        return sessions[0]


class ChatHelper(ActivityHelper):
    def post(self, request):
        # do some persistence stuff with the chat
        from core.realtime import chat

        # user = self.get_session(request)
        u = request.user
        if not u.is_anonymous:
            image = u.userprofile.get_sized_avatar_image(32, 32)
            user = u.userprofile.get_nice_name()
        else:
            image = settings.DEFAULT_USER_IMAGE
            user = settings.DEFAULT_USER_NAME

        chat.post_chat(request.data['user'], image, user, request.data['message'])
        return Response(request.data['message'], HTTP_201_CREATED)


class ActivityPlayHelper(ActivityHelper):
    def post(self, request):
        if 'id' in self.request.query_params:
            try:
                mix = Mix.objects.get(slug=self.request.query_params.get('id'))
                mix.add_play(request.user)
                data = {
                    'user': request.user.userprofile.get_nice_name() if request.user.is_authenticated else settings.DEFAULT_USER_NAME,
                    'date': datetime.datetime.now()
                }
                return Response(data, HTTP_201_CREATED)
            except Mix.DoesNotExist:
                pass

        return Response("Invalid URI or object does not exist", HTTP_400_BAD_REQUEST)


class UserSlugCheckHelper(Helper):
    def get(self, request):
        try:
            UserProfile.objects.get(slug=self.request.query_params.get('slug'))
            return Response(status=HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response(status=HTTP_200_OK)


class RadioHelper(Helper):
    def get(self, request):
        if 'rmix' in self.request.query_params:
            m = Mix.objects.order_by('?').first()
            ret = {
                'url': m.get_stream_url(),
                'slug': m.get_full_url(),
                'title': str(m)
            }
        elif 'np' in self.request.query_params:
            ret = ice_scrobbler.get_server_details()

        return Response(data=ret, status=HTTP_200_OK)

    def post(self, request):
        try:
            if 'action' in request.query_params:
                action = request.query_params.get('action')
                if action == 'shuffle':
                    ice_scrobbler.shuffle()
                    return Response(status=HTTP_200_OK)
                if action == 'play':
                    m = Mix.objects.get(slug=request.query_params.get('slug'))
                    item = {
                        'url': m.get_stream_url(),
                        'slug': m.get_full_url(),
                        'title': str(m)
                    }
                    ice_scrobbler.play(item)
                    return Response(status=HTTP_200_OK)
            if 'update' in request.query_params and 'url' in request.query_params:
                activity.post_activity('site:radio_changed', message={
                    'description': request.query_params.get('update'),
                    'url': request.query_params.get('url')
                })
        except Exception as ex:
            pass

        return Response(status=HTTP_400_BAD_REQUEST)
