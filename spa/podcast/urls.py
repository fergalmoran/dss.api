from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<uid>[\w\d_.-]+)/favourites/?$', 'spa.podcast.views.favourites', name='podast_favourites_slug'),
)
