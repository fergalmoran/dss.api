from optparse import make_option
import os
from django.core.management.base import NoArgsCommand, BaseCommand

from spa.models.mix import Mix
from core.tasks import create_waveform_task


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
        #Check for file in mix directory
        processed_file = ""
        try:
            processed_file = mix.get_absolute_path()
            if not os.path.isfile(processed_file):
                processed_file = mix.get_cache_path()
                if not os.path.isfile(processed_file):
                    print "File for [%s] not found tried\n\t%s\n\t%s" % (mix.title, processed_file, processed_file)
                    return ""

        except Exception, ex:
            print "Error generating waveform: %s" % ex.message

        return processed_file

    def handle(self, *args, **options):
        print "Scanning for missing waveforms"
        unprocessed = Mix.objects.filter(waveform_generated=False)
        for mix in unprocessed:
            print "Found %s" % mix.slug
            mix_file = self._get_file(mix)

            if mix_file is not "":
                if options['nocelery']:
                    create_waveform_task(in_file=mix_file, uid=mix.uid)
                else:
                    create_waveform_task.delay(in_file=mix_file, uid=mix.uid)

