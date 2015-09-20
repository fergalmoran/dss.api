import os
import logging

from celery import Celery
from celery.schedules import crontab
from spa import tasks

logger = logging.getLogger('dss')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dss.settings')

from django.conf import settings
app = Celery('dss')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, tasks.play_pending_audio.s('hello'), name='add every 10')
