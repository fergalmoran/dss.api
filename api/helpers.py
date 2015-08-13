import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
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

        #user = self.get_session(request)
        u = request.user
        if not u.is_anonymous():
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
                    'user': request.user.userprofile.get_nice_name() if request.user.is_authenticated() else settings.DEFAULT_USER_NAME,
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
