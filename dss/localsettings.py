import os
import ast

DEBUG = ast.literal_eval(os.environ.get('IS_DEBUG', 'True'))

DSS_TEMP_PATH = os.environ.get('DSS_TEMP_PATH', '/tmp/')
DSS_LAME_PATH = os.environ.get('DSS_LAME_PATH', '/usr/bin/sox')
DSS_WAVE_PATH = os.environ.get('DSS_WAVE_PATH',
                               '/home/fergalm/dev/personal/deepsouthsounds.com/dss.lib/wav2png/bin/Linux/wav2png')
GEOIP_PATH = os.environ.get('GEOIP_PATH', '/home/fergalm/Dropbox/Private/deepsouthsounds.com/working/geolite')

DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'deepsouthsounds')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'deepsouthsounds')
DATABASE_USER = os.environ.get('DATABASE_USER', 'deepsouthsounds')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')

STATIC_URL = '/assets/'

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/mnt/dev/deepsouthsounds.com/media')
STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/fergalm/dev/personal/deepsouthsounds.com/cache/static')
CACHE_ROOT = os.environ.get('CACHE_ROOT', '/mnt/dev/deepsouthsounds.com/cache')

MEDIA_URL = os.environ.get('MEDIA_URL', 'http://localhost/DSSMedia/')  # '{0}media/'.format(CDN_URL)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_ACCEPT_CONTENT = ['pickle', 'msgpack', 'json']

SECRET_KEY = os.environ.get('SECRET_KEY', '')
LIVE_ENABLED = os.environ.get('LIVE_ENABLED', False)

ICE_HOST = os.environ.get('ICE_HOST', 'localhost')
ICE_MOUNT = os.environ.get('ICE_MOUNT =', 'dss')
ICE_PORT = os.environ.get('ICE_PORT', 8000)

RADIO_HOST = os.environ.get('RADIO_HOST', 'localhost')
RADIO_PORT = os.environ.get('RADIO_PORT', 8888)

MANDRILL_API_KEY = os.environ.get('MANDRILL_API_KEY', '')

FACEBOOK_API_VERSION = os.environ.get('FACEBOOK_API_VERSION', '2.5')
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS',
                                    '/home/fergalm/dev/personal/deepsouthsounds.com/dss.api/googleapikey.json')
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', '')

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY', '')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET', '')
TWITTER_CALLBACK_URL = os.environ.get('TWITTER_CALLBACK_URL',
                                      'http://ext-test.deepsouthsounds.com/_login/?backend=twitter')

SOCIAL_AUTH_GOOGLE_OAUTH_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH_SECRET', '')

SOCIAL_AUTH_GOOGLE_PLUS_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_PLUS_KEY', '')
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_PLUS_SECRET', '')

DSS_DB_BACKUP_KEY = os.environ.get('DSS_DB_BACKUP_KEY', '')
DSS_DB_BACKUP_SECRET = os.environ.get('DSS_DB_BACKUP_SECRET', '')
DSS_DB_BACKUP_TOKEN = os.environ.get('DSS_DB_BACKUP_TOKEN', '')

AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', '')

if DEBUG:
    from dss.devsettings import *
