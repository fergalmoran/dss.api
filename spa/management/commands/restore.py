from django.core.management.base import LabelCommand
import dropbox
from dss import settings


def _restore_database():
    """ find latest database backup """
    client = dropbox.client.DropboxClient(settings.DSS_DB_BACKUP_TOKEN)


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
