# Django settings for dss project.
import os
import mimetypes
from datetime import timedelta
from django.core.urlresolvers import reverse_lazy
from django.conf import global_settings
from dss import storagesettings

from utils import here

from dss.localsettings import *
from dss.storagesettings import *
from dss.paymentsettings import *
from dss.logsettings import *
from dss.psa import *
from dss.celerysettings import *

DEVELOPMENT = DEBUG

TEMPLATE_DEBUG = DEBUG
VERSION = '2.13.02'

ADMINS = (
    ('Fergal Moran', 'fergal.moran@gmail.com'),
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
    }
}
import sys

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

ROOT_URLCONF = 'dss.urls'
TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-ie'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
s = True

SITE_ROOT = here('')

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    here('static'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django_facebook.context_processors.facebook',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
    # 'spa.middleware.uploadify.SWFUploadMiddleware',
    # 'spa.middleware.sqlprinter.SqlPrintingMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

WSGI_APPLICATION = 'dss.wsgi.application'
TEMPLATE_DIRS = (here('templates'),)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    # 'django_facebook',
    'django_extensions',
    'django_gravatar',

    # TODO: remove
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    'corsheaders',
    'sorl.thumbnail',
    'djcelery',
    'spa',
    'gunicorn',
    'spa.signals',
    'core',
    'storages',
    'social.apps.django_app.default',

    'djrill',
    'rest_framework',
    'rest_framework.authtoken',
)

# where to redirect users to after logging in
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('home')

FACEBOOK_APP_ID = '154504534677009'

AVATAR_STORAGE_DIR = MEDIA_ROOT + '/avatars/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

INTERNAL_IPS = ('127.0.0.1', '86.44.166.21', '192.168.1.111')

TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
TASTYPIE_ALLOW_MISSING_SLASH = True

SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'mixes')
SENDFILE_URL = '/media/mixes'

# SESSION_ENGINE = 'django.contrib.sessions.models.Session'

mimetypes.add_type("text/xml", ".plist", False)

HTML_MINIFY = not DEBUG

DEFAULT_FROM_EMAIL = 'DSS ChatBot <chatbot@deepsouthsounds.com>'
DEFAULT_HTTP_PROTOCOL = 'http'

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

if DEBUG:
    import mimetypes

    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("application/x-font-woff", ".woff", True)
    mimetypes.add_type("application/vnd.ms-fontobject", ".eot", True)
    mimetypes.add_type("font/ttf", ".ttf", True)
    mimetypes.add_type("font/otf", ".otf", True)

REALTIME_HEADERS = {
    'content-type': 'application/json'
}


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'PAGINATE_BY': 12,  # Default to 10
    'PAGINATE_BY_PARAM': 'limit',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100  # Maximum limit allowed when using `?page_size=xxx`.}
}

DEFAULT_TRACK_IMAGE = 'assets/images/dyn/default-track-200.png'
DEFAULT_USER_IMAGE = 'assets/images/dyn/default-avatar-32.png'
DEFAULT_USER_NAME = 'Anonymouse'
DEFAULT_USER_TITLE = 'Just another DSS lover'
DEFAULT_WAVEFORM_GENERATING = '/assets/images/waveform-interstitial.gif'

SITE_NAME = 'Deep South Sounds'
THUMBNAIL_PREFIX = '_tn/'

# THUMBNAIL_STORAGE = 'storages.backends.azure_storage.AzureStorage'

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(seconds=900),
    # 'JWT_EXPIRATION_DELTA': timedelta(seconds=5),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
}

""" static settings """
CDN_URL = storagesettings.AZURE_ITEM_BASE_URL
MIXIMAGE_URL = '{0}miximages/'.format(CDN_URL)
WAVEFORM_URL = '{0}waveforms/'.format(CDN_URL)
STREAM_URL = '{0}mixes/'.format(CDN_URL)
AUDIO_URL = '{0}mixes/'.format(CDN_URL)


NOTIFICATIONS_FROM_ADDRESS = "admin@deepsouthsounds.com"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'cache-control',
    'accept',
    'origin',
    'authorization',

    'upload-hash',
    'session-id',
    'auth-backend',
    'x-csrftoken'
)

""" End static settings """