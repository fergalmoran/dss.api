# e Django settings for dss project.
import os
import mimetypes
from django.core.urlresolvers import reverse_lazy
import djcelery
from django.conf import global_settings

from dss import logsettings
from utils import here

from localsettings import *
from storagesettings import *
from paymentsettings import *
from psa import *

DEVELOPMENT = DEBUG

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fergal Moran', 'fergal.moran@gmail.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'spa.UserProfile'

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deepsouthsounds',
        'ADMINUSER': 'postgres',
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
    }
}
import sys

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    print "Testing"
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


    # TODO: remove..
    # `allauth` specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'spa.middleware.uploadify.SWFUploadMiddleware',
     #'spa.middleware.sqlprinter.SqlPrintingMiddleware' if DEBUG else None,
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

WSGI_APPLICATION = 'dss.wsgi.application'
TEMPLATE_DIRS = (here('templates'),)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'user_sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    #'django_facebook',
    'django_extensions',
    'django_gravatar',
    'djcelery',
    'corsheaders',
    'sorl.thumbnail',
    'spa',
    'spa.signals',
    'core',
    #'schedule',
    'django_user_agents',

    'social.apps.django_app.default',

    # TODO: remove
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'south',

    'dbbackup',
    'djrill',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
)

# where to redirect users to after logging in
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('home')

LOGGING = logsettings.LOGGING

FACEBOOK_APP_ID = '154504534677009'

djcelery.setup_loader()

AVATAR_STORAGE_DIR = MEDIA_ROOT + '/avatars/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

INTERNAL_IPS = ('127.0.0.1', '86.44.166.21', '192.168.1.111')

TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
TASTYPIE_ALLOW_MISSING_SLASH = True

SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'mixes')
SENDFILE_URL = '/media/mixes'

SESSION_ENGINE = 'user_sessions.backends.db'

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
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass

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
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGINATE_BY': 12,  # Default to 10
    'PAGINATE_BY_PARAM': 'limit',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100  # Maximum limit allowed when using `?page_size=xxx`.}
}


DEFAULT_USER_IMAGE = 'assets/images/default-avatar-32.png'
DEFAULT_USER_NAME = 'Anonymouse'
DEFAULT_USER_TITLE = 'Just another DSS lover'


SITE_NAME = 'Deep South Sounds'
