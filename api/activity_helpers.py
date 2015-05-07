from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from dss import settings
from spa.models import Mix


class ActivityHelper(APIView):
    pass


class ActivityPlayHelper(ActivityHelper):
    def post(self, request):
        if 'id' in self.request.QUERY_PARAMS:
            try:
                mix = Mix.objects.get(slug=self.request.QUERY_PARAMS.get('id'))
                mix.add_play(request.user)
                data = {
                    'user': request.user.get_nice_name() if request.user.is_authenticated() else settings.DEFAULT_USER_NAME,
                    'date': mix.description
                }
                return Response(data, HTTP_201_CREATED)
            except Mix.DoesNotExist:
                pass

        return Response("Invalid URI or object does not exist", HTTP_400_BAD_REQUEST)
