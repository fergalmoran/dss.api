from dss import localsettings
import os

print("Importing storage settings")

AZURE_ACCOUNT_NAME = os.environ.get('CDN_NAME', 'dsscdn2')
AZURE_CONTAINER = 'media'
AZURE_ACCOUNT_KEY = localsettings.AZURE_ACCOUNT_KEY
AZURE_ITEM_BASE_URL = 'https://{}.blob.core.windows.net/'.format(AZURE_ACCOUNT_NAME)