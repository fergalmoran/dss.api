from django.core.management.base import LabelCommand, CommandError
from subprocess import Popen, PIPE, STDOUT
from dss import settings
import tarfile
import dropbox
import os, time


def _backup_database():
    print("Creating database backup")
    args = []
    args += ["--username=%s" % settings.DATABASE_USER]
    args += ["--password"]
    args += ["--host=%s" % settings.DATABASE_HOST]
    args += [settings.DATABASE_NAME]
    remote_file = "{0}.tar.gz".format(time.strftime("%Y%m%d-%H%M%S"))

    pipe = Popen('pg_dump %s > %s' % (' '.join(args), remote_file), shell=True, stdin=PIPE)

    if settings.DATABASE_PASSWORD:
        output = pipe.communicate(input=bytes(settings.DATABASE_PASSWORD + '\n', 'UTF-8'))
        print(output)

    _create_backup_bundle(remote_file, 'databases', settings.PROJECT_ROOT)


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
    tar.add(location, arcname=remote_file, filter=_progress_filter)
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
