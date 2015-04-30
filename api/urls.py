from api.auth import ObtainAuthToken, ObtainUser, ObtainLogout
from api.views import CommentViewSet, MixViewSet, UserProfileViewSet, NotificationViewSet, PartialMixUploadView, \
    GenreViewSet, ActivityViewSet, HitlistViewset, AttachedImageUploadView, DownloadItemView, SearchResultsView
from django.conf.urls import url, patterns, include
from rest_framework_nested import routers

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'notification', NotificationViewSet)
router.register(r'hitlist', HitlistViewset)
router.register(r'comments', CommentViewSet)
router.register(r'user', UserProfileViewSet, base_name='userprofile')
router.register(r'activity', ActivityViewSet, base_name='activity')

router.register(r'mix', MixViewSet)
mix_router = routers.NestedSimpleRouter(router, r'mix', lookup='mix')
mix_router.register('comments', CommentViewSet)

"""
router.register(r'hitlist', HitlistViewset, base_name='hitlist')
router.register(r'notification', NotificationViewSet, base_name='notification')
"""
router.register(r'genre', GenreViewSet, base_name='genre')
urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^', include(mix_router.urls)),
    url(r'_download/', DownloadItemView.as_view()),
    url(r'_upload/$', PartialMixUploadView.as_view()),
    url(r'_image/$', AttachedImageUploadView.as_view()),
    url(r'_search/$', SearchResultsView.as_view()),
    url(r'^', include(router.urls)),

    url(r'^login/', ObtainAuthToken.as_view()),
    url(r'^user/', ObtainUser.as_view()),
    url(r'^logout/', ObtainLogout.as_view()),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
