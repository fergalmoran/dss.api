from dss import localsettings
import os

DEBUG_AZURE_ACCOUNT_NAME = os.environ.get('CDN_NAME', 'dsscdn')
AZURE_ACCOUNT_NAME = os.environ.get('CDN_NAME', 'dsscdn2')
AZURE_CONTAINER = 'media'
AZURE_ACCOUNT_KEY = localsettings.AZURE_ACCOUNT_KEY
AZURE_ITEM_BASE_URL = 'https://{}.blob.core.windows.net/'.format(AZURE_ACCOUNT_NAME)
