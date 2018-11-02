from django.conf.urls import url

from spa.podcast.views import favourites, following, user, featured

urlpatterns = [
    url(r'^(?P<uid>[\w\d_.-]+)/favourites/?$', favourites, name='podcast_favourites_slug'),
    url(r'^(?P<uid>[\w\d_.-]+)/following/?$', following, name='podcast_following_slug'),
    url(r'^(?P<slug>[\w\d_.-]+)/?$', user, name='podast_user_slug'),
    url(r'', featured, name='`podcast_featured_slug'),
]
