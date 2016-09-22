from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^blog/(?P<slug>[\w\d_.-]+)/?$', 'spa.blog.views.entry', name='blog_entry_slug'),
    url(r'^$', 'spa.blog.views.index', name='blog_index')
)
