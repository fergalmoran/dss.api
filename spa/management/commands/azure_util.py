import os
from django.core.management.base import LabelCommand, CommandError
import sys

from core.utils import cdn
from spa.models.mix import Mix


def _update_azure_headers():
    ms = Mix.objects.all()
    for m in ms:
        print("Update headers for {0}".format(m.title))
        cdn.set_azure_details(
            blob_name='{0}.mp3'.format(m.uid),
            download_name='Deep South Sounds - {0}.mp3'.format(m.title),
            container_name='mixes')


def _check_missing_mixes():
    ms = Mix.objects.all()
    found = 0
    for m in ms:
        url = m.get_download_url()
        if not cdn.file_exists(url):
            file = '/mnt/dev/working/deepsouthsounds.com/media/mixes/{0}.mp3'.format(m.uid)
            if os.path.isfile(file):
                print(('* {0}'.format(file)))
                # cdn.upload_file_to_azure(file, '{0}.mp3'.format(m.uid), 'mixes')
                found += 1
            else:
                found += 1
                print(('({0}){1} - {2}'.format(found, m.slug, m.uid)))

    print(('{0} of {1} missing'.format(found, Mix.objects.count())))


class Command(LabelCommand):
    def handle_label(self, label, **options):
        pass

    def upload_mix(self, **options):
        try:
            mixes = Mix.objects.filter(archive_updated=False)
            for mix in mixes:
                blob_name, download_name = mix.get_cdn_details()
                cdn.upload_file_to_azure(blob_name, "mp3", download_name)
                mix.archive_updated = True
                mix.save()

        except Exception as ex:
            print("Fatal error, bailing. {0}".format(ex.message))

    def handle(self, *labels, **options):
        if len(labels) != 1:
            raise CommandError('`%s` is not a valid argument' % labels)

        label = labels[0]

        if label not in ['check_missing_mixes', 'update_azure_headers']:
            raise CommandError('`%s` unknown action' % label)

        if label == 'check_missing_mixes':
            _check_missing_mixes()
        if label == 'update_azure_headers':
            _update_azure_headers()
