from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^mix/(?P<mix_id>\d+)/$', 'spa.embedding.views.mix', name='embed_mix'),
    url(r'^mix/(?P<slug>[\w\d_.-]+)/$', 'spa.embedding.views.mix', name='embed_mix_slug'),
)