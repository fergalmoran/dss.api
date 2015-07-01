from django.core.management.base import NoArgsCommand, BaseCommand

from core.utils.cdn import upload_to_azure
from spa.models import Mix


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it')

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

    def handle(self, *args, **options):
        pass
