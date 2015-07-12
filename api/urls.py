from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from api import views, auth, helpers

router = DefaultRouter()  # trailing_slash=True)

router.register(r'user', views.UserProfileViewSet)
router.register(r'mix', views.MixViewSet)


router.register(r'notification', views.NotificationViewSet)
router.register(r'hitlist', views.HitlistViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'activity', views.ActivityViewSet, base_name='activity')
router.register(r'genre', views.GenreViewSet, base_name='genre')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    # url(r'^', include(mix_router.urls)),
    url(r'_download/', views.DownloadItemView.as_view()),
    url(r'_upload/$', views.PartialMixUploadView.as_view()),
    url(r'_image/$', views.AttachedImageUploadView.as_view()),
    url(r'_search/$', views.SearchResultsView.as_view()),
    url(r'^', include(router.urls)),

    url(r'^login/', auth.ObtainAuthToken.as_view()),
    url(r'^logout/', auth.ObtainLogout.as_view()),

    # url(r'^_tr/', RefreshToken.as_view()),
    url(r'^__u/checkslug', helpers.UserSlugCheckHelper.as_view()),
    url(r'^__u/', auth.ObtainUser.as_view()),


    url(r'^_act/play', helpers.ActivityPlayHelper.as_view()),
    url(r'^_chat/', helpers.ChatHelper.as_view()),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
