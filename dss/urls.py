from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from dss import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^__redir/blog/', include('spa.blog.urls')),
    (r'^__redir/social/', include('spa.social.urls')),
    (r'^arges/', include('spa.social.urls')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    url(r'^', include('api.urls')),
)

if settings.DEBUG:
    from django.views.static import serve

    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns(
            '',
            (r'^%s(?P<path>.*)$' % _media_url,
             serve,
             {'document_root': settings.MEDIA_ROOT}))
    del (_media_url, serve)
