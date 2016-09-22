import os
import sys

path = '/var/www/deepsouthsounds.com/dss'
if path not in sys.path:
    sys.path.append(path)

path = '/var/www/deepsouthsounds.com'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'dss.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
