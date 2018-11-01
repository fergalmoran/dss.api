from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from dss import settings

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^_embed/', include('spa.embedding.urls')),
    url(r'^__redir/blog/', include('spa.blog.urls')),
    url(r'^__redir/social/', include('spa.social.urls')),
    url(r'^podcasts/', include('spa.podcast.urls')),
    url(r'^podcast/', include('spa.podcast.urls')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    url(r'^', include('api.urls'))
]

if settings.DEBUG:
    from django.views.static import serve

    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += [
            (r'^%s(?P<path>.*)$' % _media_url,
             serve,
             {'document_root': settings.MEDIA_ROOT})
        ]
    del (_media_url, serve)
