from django.conf.urls import patterns, url, include
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api import views, auth, helpers
from api.auth import SocialLoginHandler
from core.realtime import activity

router = DefaultRouter()  # trailing_slash=True)


router.register(r'notification', views.NotificationViewSet)
router.register(r'hitlist', views.HitlistViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'activity', views.ActivityViewSet, base_name='activity')
router.register(r'genre', views.GenreViewSet, base_name='genre')
router.register(r'messages', views.MessageViewSet, base_name='messages')
router.register(r'shows', views.ShowViewSet, base_name='shows')
router.register(r'blog', views.BlogViewSet, base_name='shows')
router.register(r'playlist', views.PlaylistViewSet, base_name='playlists')
router.register(r'playlist', views.PlaylistViewSet, base_name='playlists')

router.register(r'user', views.UserProfileViewSet)
router.register(r'mix', views.MixViewSet)

class DebugView(APIView):
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        print(self.request.session)
        return Response({'status': 'ok', 'session': self.request.session.session_key},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            activity.post_activity(
                channel='user:broadcast',
                message='Hello Sailor',
                session=2,
                # session=request.user.userprofile.get_session_id(),
            )
        except Exception as ex:
            print(ex)

        return Response({
            'status': 'Hello',
            'message': 'Sailor'
        }, status=status.HTTP_200_OK)


urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'_download/', views.DownloadItemView.as_view()),
    url(r'_upload/$', views.PartialMixUploadView.as_view()),
    url(r'_image/$', views.AttachedImageUploadView.as_view()),
    url(r'_search/$', views.SearchResultsView.as_view()),
    url(r'^', include(router.urls)),

    url(r'^_login/?$', SocialLoginHandler.as_view()),
    url(r'^_a?$', SocialLoginHandler.as_view()),
    url(r'^token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),

    url(r'^__u/checkslug', helpers.UserSlugCheckHelper.as_view()),
    url(r'^__u/', auth.ObtainUser.as_view()),

    url(r'^_act/play', helpers.ActivityPlayHelper.as_view()),
    url(r'^_chat/', helpers.ChatHelper.as_view()),

    url(r'^_radio', helpers.RadioHelper.as_view()),

    url(r'^__debug/', DebugView.as_view()),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
