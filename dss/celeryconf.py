from __future__ import absolute_import

import os
import logging

from celery import Celery

logger = logging.getLogger('dss')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dss.settings')

from django.conf import settings
print 'Connecting to celery app'
app = Celery('dss')
print 'Connected'

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
print 'Discovered tasks'
