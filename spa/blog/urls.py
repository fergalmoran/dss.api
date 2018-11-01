from django.conf.urls import url

from spa.blog.views import entry, index

urlpatterns = [
    url(r'^blog/(?P<slug>[\w\d_.-]+)/?$', entry, name='blog_entry_slug'),
    url(r'^$', index, name='blog_index')
]
