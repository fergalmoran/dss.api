from gzip import GzipFile
import subprocess
from django.core.management.base import LabelCommand, CommandError
from subprocess import Popen, PIPE, STDOUT
import pexpect
from dss import settings
import tarfile
import dropbox
import os, time


def _backup_database():
    print("Creating database backup")
    file_name = "{0}.sql".format(time.strftime("%Y%m%d-%H%M%S"))
    backup_file = os.path.join(settings.DSS_TEMP_PATH, file_name)

    print('Backing up {} database to {}'.format(settings.DATABASE_NAME, file_name))
    command = '/usr/bin/pg_dump --username {} --host {} --password {}'.format(
        settings.DATABASE_USER, settings.DATABASE_HOST, settings.DATABASE_NAME)

    child = pexpect.spawnu(command)
    fout = open(backup_file, "w")
    child.logfile = fout
    child.expect("[Pp]assword:")
    child.sendline(settings.DATABASE_PASSWORD)
    child.expect(pexpect.EOF)

    _create_backup_bundle("{0}.tar.gz".format(file_name), 'database', backup_file)


def _backup_settings():
    print("Creating settings backup")
    file_name = "{0}.tar.gz".format(time.strftime("%Y%m%d-%H%M%S"))
    _create_backup_bundle(file_name, 'settings', settings.PROJECT_ROOT)


def _progress_filter(tarinfo):
    print("Adding: {}".format(tarinfo.name, 0, 1))
    return tarinfo


def _create_backup_bundle(remote_file, type, location):
    backup_file = "{0}/{1}".format(settings.DSS_TEMP_PATH, remote_file)

    tar = tarfile.open(backup_file, "w:gz")
    tar.add(location)
    tar.close()

    _upload_to_dropbox(type, backup_file, remote_file)


def _upload_to_dropbox(type, backup_file, remote_file):
    print("Uploading {0} to dropbox".format(backup_file))
    with open(backup_file, "rb") as f:
        client = dropbox.client.DropboxClient(settings.DSS_DB_BACKUP_TOKEN)
        response = client.put_file("{0}/{1}".format(type, remote_file), f, overwrite=True)

        os.remove(backup_file)

        print(response)


def _backup_media():
    print("Creating media backup")
    file_name = "{0}.tar.gz".format(time.strftime("%Y%m%d-%H%M%S"))
    _create_backup_bundle(file_name, 'media', settings.MEDIA_ROOT)


class Command(LabelCommand):
    help = (
        "Handles thumbnails and key value store"
    )
    missing_args_message = "Enter one of [database, settings, media, all]"

    def handle_label(self, label, **options):
        if label == "database":
            _backup_database()
        if label == "settings":
            _backup_settings()
        if label == "media":
            _backup_media()
        if label == "all":
            _backup_database()
            _backup_settings()
            _backup_media()
