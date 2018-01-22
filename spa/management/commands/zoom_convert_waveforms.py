import os
from django.core.management.base import NoArgsCommand
from core.utils.waveform import generate_waveform
from dss import settings
from spa.models.mix import Mix
from . import helpers

class Command(NoArgsCommand):

    def _convert_remote(self):
        mixes = Mix.objects.exclude(waveform_version=2)
        for mix in mixes:
            # download audio file to temp path
            print("Starting to process: %s" % mix.slug)
            file_name = "/tmp/%s.mp3" % mix.uid
            url = mix.get_stream_url()
            print("Downloading: %s To: %s" % (url, file_name))
            helpers.download_file(url, file_name)
            if not os.path.isfile(file_name):
                print("File failed to download")
            else:
                # process waveform
                generate_waveform(file_name, )
                # update mix.waveform_version to 2

                # delete cached file
                os.remove(file_name)
                print("Done %s" % mix.slug)

    def handle_noargs(self, **options):
        try:
            mixes = Mix.objects.exclude(waveform_version=2)
            for mix in mixes:
                from PIL import Image
                import glob

                output_file = '{0}/waveforms/{1}.{2}'.format(settings.MEDIA_ROOT, mix.uid, 'png')
                if os.path.exists(output_file):
                    try:
                        print('Processing: %s' % mix.slug)
                        im = Image.open(output_file)
                        w, h = im.size
                        im.crop((0, 0, w, h / 2)).save(output_file)
                    except Exception:
                        print("Exception with image: %s" % output_file)
                else:
                    print("Skipping: %s" % mix.slug)
                mix.waveform_version = 2
                mix.save()
                pass
        except Exception as ex:
            print("Debug exception: %s" % ex)