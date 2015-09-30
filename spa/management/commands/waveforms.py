from optparse import make_option
import os

from django.core.management.base import BaseCommand
from spa import tasks

from spa.management.commands import helpers
from spa.models.mix import Mix
from spa.tasks import create_waveform_task


class Command(BaseCommand):
    help = "Generate all outstanding waveforms"
    option_list = BaseCommand.option_list + (
        make_option('--nocelery',
                    action='store_true',
                    dest='nocelery',
                    default=False,
                    help='Dispatch calls to celery broker'),
    )

    @staticmethod
    def _get_file(mix):
        try:
            if mix.archive_updated:
                print("Mix is archived: boo hoo")
                file_name = "/tmp/%s.mp3" % mix.uid
                url = mix.get_stream_url()
                print("Downloading: %s To: %s" % (url, file_name))
                helpers.download_file(url, file_name)
                if not os.path.isfile(file_name):
                    print("File failed to download")
                else:
                    return file_name
            else:
                processed_file = mix.get_absolute_path()
                if not os.path.isfile(processed_file):
                    processed_file = mix.get_cache_path()
                    if not os.path.isfile(processed_file):
                        print("File for [%s] not found tried\n\t%s\n\t%s" % (mix.title, processed_file, processed_file))
                        return ""
                return processed_file

        except Exception as ex:
            print("Error generating waveform: {0}".format(ex.message))

        return ""

    def handle(self, *args, **options):
        print("Scanning for missing waveforms")
        unprocessed = Mix.objects.filter(waveform_generated=False)
        for mix in unprocessed:
            print("Found %s" % mix.slug)
            mix_file = self._get_file(mix)

            if mix_file is not "":
                if options['nocelery']:
                    create_waveform_task(in_file=mix_file, uid=mix.uid)
                else:
                    (
                        tasks.create_waveform_task.s(mix_file, mix.uid) |
                        tasks.upload_to_cdn_task.subtask(('mp3', mix.uid, 'mixes'), immutable=True) |
                        tasks.upload_to_cdn_task.subtask(('png', mix.uid, 'waveforms'), immutable=True)
                    ).delay()

