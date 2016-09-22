from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^playlist/(?P<slug>[\w\d_.-]+)/?$', 'spa.social.views.playlist', name='social_playlist_slug'),
    url(r'^mix/(?P<slug>[\w\d_.-]+)/?$', 'spa.social.views.facebook_mix', name='social_mix_slug'),
    url(r'^user/(?P<user_id>\w+)/?$', 'spa.social.views.user', name='social_user'),
    url(r'^like/(?P<mix_id>\d+)/?$', 'spa.social.views.post_like', name='social_like'),
    url(r'^$', 'spa.social.views.index', name='social_index')
)