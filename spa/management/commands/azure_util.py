import os
from django.core.management.base import BaseCommand

from core.utils import cdn
from spa.models import Mix


def _check_missing_mixes():
    ms = Mix.objects.all()
    found = 0
    for m in ms:
        url = m.get_download_url()
        if not cdn.file_exists(url):
            file = '/mnt/dev/deepsouthsounds.com/media/mixes/{0}.mp3'.format(m.uid)
            if os.path.isfile(file):
                print '* {0}'.format(file)
                cdn.upload_file_to_azure(file, '{0}.mp3'.format(m.uid), 'mixes')
                found += 1
            else:
                found += 1
                print '({0}){1} - {2}'.format(found, m.slug, m.uid)

    print '{0} of {1} missing'.format(found, Mix.objects.count())


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
                cdn.upload_file_to_azure(blob_name, "mp3", download_name)
                mix.archive_updated = True
                mix.save()

        except Exception, ex:
            print "Fatal error, bailing. {0}".format(ex.message)

    def handle(self, *args, **options):
        if len(args) == 0:
            print "Commands are \n\t_check_missing_mixes"
        elif args[0] == 'check_missing_mix':
            _check_missing_mixes()
        else:
            print "Commands are \n\tcheck_missing_mix"
