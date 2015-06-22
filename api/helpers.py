import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from dss import settings
from spa.models import Mix, UserProfile


class Helper(APIView):
    pass


class ActivityHelper(APIView):
    pass


class ActivityPlayHelper(ActivityHelper):
    def post(self, request):
        if 'id' in self.request.QUERY_PARAMS:
            try:
                mix = Mix.objects.get(slug=self.request.QUERY_PARAMS.get('id'))
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
            UserProfile.objects.get(slug=self.request.QUERY_PARAMS.get('slug'))
            return Response(status=HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response(status=HTTP_200_OK)
