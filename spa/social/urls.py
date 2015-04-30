from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^playlist/(?P<slug>[\w\d_.-]+)/$', 'spa.social.views.playlist', name='social_playlist_slug'),
    url(r'^redirect/mix/(?P<mix_id>\d+)/$', 'spa.social.views.mix', name='social_redirect_mix'),
    url(r'^redirect/mix/(?P<slug>[\w\d_.-]+)/$', 'spa.social.views.mix', name='social_redirect_mix_slug'),
    url(r'^mix/(?P<mix_id>\d+)/$', 'spa.social.views.mix', name='social_mix'),
    url(r'^mix/(?P<slug>[\w\d_.-]+)/$', 'spa.social.views.mix', name='social_mix_slug'),
    url(r'^user/(?P<user_id>\w+)/$', 'spa.social.views.user', name='social_user'),
    url(r'^like/(?P<mix_id>\d+)/$', 'spa.social.views.post_like', name='social_like'),
    url(r'^$', 'spa.social.views.index', name='social_index')
)