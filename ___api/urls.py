from ___api import views
from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserProfileViewSet)
router.register(r'mix', views.MixViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
