from django.conf.urls import patterns, url, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from api import views, auth, helpers
from api.auth import FacebookView
from rest_framework.views import status
from rest_framework.response import Response

router = DefaultRouter()  # trailing_slash=True)

router.register(r'user', views.UserProfileViewSet)
router.register(r'mix', views.MixViewSet)

router.register(r'notification', views.NotificationViewSet)
router.register(r'hitlist', views.HitlistViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'activity', views.ActivityViewSet, base_name='activity')
router.register(r'genre', views.GenreViewSet, base_name='genre')


class DebugView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        return Response({
            'status': 'Hello',
            'message': 'Sailor'
        }, status=status.HTTP_200_OK)


urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    # url(r'^', include(mix_router.urls)),
    url(r'_download/', views.DownloadItemView.as_view()),
    url(r'_upload/$', views.PartialMixUploadView.as_view()),
    url(r'_image/$', views.AttachedImageUploadView.as_view()),
    url(r'_search/$', views.SearchResultsView.as_view()),
    url(r'^', include(router.urls)),

    url(r'^_login/', FacebookView.as_view()),
    url(r'^token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),

    # url(r'^_tr/', RefreshToken.as_view()),
    url(r'^__u/checkslug', helpers.UserSlugCheckHelper.as_view()),
    url(r'^__u/', auth.ObtainUser.as_view()),

    url(r'^_act/play', helpers.ActivityPlayHelper.as_view()),
    url(r'^_chat/', helpers.ChatHelper.as_view()),


    url(r'^__debug/', DebugView.as_view()),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
