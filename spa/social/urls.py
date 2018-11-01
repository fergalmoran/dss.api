from django.conf.urls import url

from spa.social.views import playlist, facebook_mix, user, post_like, index

urlpatterns = [
    url(r'^playlist/(?P<slug>[\w\d_.-]+)/?$', playlist, name='social_playlist_slug'),
    url(r'^mix/(?P<slug>[\w\d_.-]+)/?$', facebook_mix, name='social_mix_slug'),
    url(r'^user/(?P<user_id>\w+)/?$', user, name='social_user'),
    url(r'^like/(?P<mix_id>\d+)/?$', post_like, name='social_like'),
    url(r'^$', index, name='social_index')
]