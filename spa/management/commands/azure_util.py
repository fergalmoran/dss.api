from django.core.management.base import NoArgsCommand

from core.utils.cdn import upload_to_azure
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            mixes = Mix.objects.filter(archive_updated=False)
            for mix in mixes:
                blob_name, download_name = mix.get_cdn_details()
                upload_to_azure(blob_name, "mp3", download_name)
                mix.archive_updated = True
                mix.save()

        except Exception, ex:
            print "Fatal error, bailing. {0}".format(ex.message)
