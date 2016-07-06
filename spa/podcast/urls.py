from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<uid>[\w\d_.-]+)/favourites/?$', 'spa.podcast.views.favourites', name='podast_favourites_slug'),
    url(r'^(?P<uid>[\w\d_.-]+)/following/?$', 'spa.podcast.views.following', name='podast_following_slug'),
    url(r'^(?P<slug>[\w\d_.-]+)/?$', 'spa.podcast.views.user', name='podast_user_slug'),
    url(r'^/?$', 'spa.podcast.views.featured', name='podast_featured_slug'),
)
