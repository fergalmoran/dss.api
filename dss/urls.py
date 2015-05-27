from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from dss import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/v2/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^grappelli/', include('grappelli.urls')),
)
handler500 = 'spa.views.debug_500'

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
