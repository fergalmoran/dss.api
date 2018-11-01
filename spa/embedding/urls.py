from django.conf.urls import url

from spa.embedding.views import mix

urlpatterns = [
    url(r'^mix/(?P<mix_id>\d+)/$', mix, name='embed_mix'),
    url(r'^mix/(?P<slug>[\w\d_.-]+)/$', mix, name='embed_mix_slug'),
]