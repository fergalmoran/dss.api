import os
import tarfile

from django.core.management.base import LabelCommand
import dropbox
from dss import settings
import sys

from utils import query_yes_no



def _restore_database():
    """ find latest database backup """
    client = dropbox.Dropbox(settings.DSS_DB_BACKUP_TOKEN)
    files = client.files_list_folder('/media')
    latest = None
    for f in files.entries:
        print(f.server_modified)
        if latest is None or f.server_modified > latest.server_modified:
            latest = f

    if latest is not None:
        #if query_yes_no("Restoring backing from: {}\nProceed (y/n?)".format(latest)):
        print("Restoring database")
        backup_file = '/tmp/{}'.format(latest.name)
        result = client.files_download_to_file(backup_file, latest.path_lower)
        print("Downloaded {}".format(result))

        if os.path.exists(backup_file):
            print("Download completed")
            o = tarfile.open(backup_file)
            o.extract()
        else:
            print("Unable to download file")


"""
import requests
...
headers = ... # set up auth
...
params = { 'list' : 'true' }
response = requests.get('https://api.dropbox.com/1/metadata/dropbox/<directory>', params=params, headers=headers)
subdirs = [d['path'] for d in response.json()['contents'] if d['is_dir'] == True]
print(subdirs)
"""


class Command(LabelCommand):
    help = (
        "Handles restoring of items backed up"
    )
    missing_args_message = "Enter one of [database, settings, media, all]"

    def handle_label(self, label, **options):
        if label == "database":
            _restore_database()
        if label == "settings":
            pass
        if label == "media":
            pass
        if label == "all":
            _restore_database()
