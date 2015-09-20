from gzip import GzipFile
import subprocess
from django.core.management.base import LabelCommand, CommandError
from subprocess import Popen, PIPE, STDOUT
from dropbox.rest import ErrorResponse
import pexpect
from dss import settings
import tarfile
import dropbox
import os, time

from dropbox.client import ChunkedUploader

""" Monkey patch dropbox upload chunked """


def __upload_chunked(self, chunk_size = 4 * 1024 * 1024):
    """Uploads data from this ChunkedUploader's file_obj in chunks, until
    an error occurs. Throws an exception when an error occurs, and can
    be called again to resume the upload.

    Parameters
        chunk_size
          The number of bytes to put in each chunk. (Default 4 MB.)
    """

    while self.offset < self.target_length:
        next_chunk_size = min(chunk_size, self.target_length - self.offset)
        if self.last_block == None:
            self.last_block = self.file_obj.read(next_chunk_size)

        try:
            (self.offset, self.upload_id) = self.client.upload_chunk(
                self.last_block, next_chunk_size, self.offset, self.upload_id)
            self.last_block = None
        except ErrorResponse as e:
            # Handle the case where the server tells us our offset is wrong.
            must_reraise = True
            if e.status == 400:
                reply = e.body
                if "offset" in reply and reply['offset'] != 0 and reply['offset'] > self.offset:
                    self.last_block = None
                    self.offset = reply['offset']
                    must_reraise = False
            if must_reraise:
                raise

ChunkedUploader.upload_chunked = __upload_chunked


def _backup_database():
    print("Creating database backup")
    file_name = "{}.sql".format(time.strftime("%Y%m%d-%H%M%S"))
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

    zip_name = "{0}.tar.gz".format(file_name)
    archive = _create_backup_bundle(zip_name, backup_file)
    _upload_to_dropbox('database', archive, zip_name)


def _backup_settings():
    print("Creating settings backup")
    zip_name = "{0}.tar.gz".format(time.strftime("%Y%m%d-%H%M%S"))
    tar_file = _create_backup_bundle(zip_name, settings.PROJECT_ROOT)
    _upload_to_dropbox('settings', tar_file, "{}.tar.gz".format(zip_name))


def _progress_filter(tarinfo):
    print("Adding: {}".format(tarinfo.name, 0, 1))
    return tarinfo


def _create_backup_bundle(remote_file, location):
    backup_file = "{0}/{1}".format(settings.DSS_TEMP_PATH, remote_file)

    tar = tarfile.open(backup_file, "w:gz")
    tar.add(location)
    tar.close()
    return backup_file


def _upload_to_dropbox(type, backup_file, remote_file):
    print("Uploading {0} to dropbox".format(backup_file))
    try:
        with open(backup_file, "rb") as f:
            client = dropbox.client.DropboxClient(settings.DSS_DB_BACKUP_TOKEN)
            response = client.put_file("{0}/{1}".format(type, remote_file), f, overwrite=True)

            os.remove(backup_file)
            print(response)
    except Exception as ex:
        print(ex)


def _backup_media():
    print("Creating media backup")
    file_name = "{0}.tar.gz".format(time.strftime("%Y%m%d-%H%M%S"))
    archive = _create_backup_bundle(file_name, settings.MEDIA_ROOT)

    size = os.path.getsize(archive)
    upload_file = open(archive, 'rb')

    client = dropbox.client.DropboxClient(settings.DSS_DB_BACKUP_TOKEN)
    uploader = client.get_chunked_uploader(upload_file, size)
    while uploader.offset < size:
        try:
            upload = uploader.upload_chunked()
        except Exception as e:
            print("Error uploading: {0}".format(e))

    uploader.finish('/media/{}'.format(file_name))


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
