import os
from django.core.management.base import NoArgsCommand
from core.utils.waveform import generate_waveform
from dss import settings
from spa.models.mix import Mix


class Command(NoArgsCommand):
    def _download_file(self, url, file_name):
        import urllib2

        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            file_buffer = u.read(block_sz)
            if not file_buffer:
                break

            file_size_dl += len(file_buffer)
            f.write(file_buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status += chr(8) * (len(status) + 1)
            print status,

        f.close()

    def _convert_remote(self):
        mixes = Mix.objects.exclude(waveform_version=2)
        for mix in mixes:
            # download audio file to temp path
            print "Starting to process: %s" % mix.slug
            file_name = "/tmp/%s.mp3" % mix.uid
            url = mix.get_stream_url()
            print "Downloading: %s To: %s" % (url, file_name)
            self._download_file(url, file_name)
            if not os.path.isfile(file_name):
                print "File failed to download"
            else:
                # process waveform
                generate_waveform(file_name, )
                # update mix.waveform_version to 2

                # delete cached file
                os.remove(file_name)
                print "Done %s" % mix.slug

    def handle_noargs(self, **options):
        try:
            mixes = Mix.objects.exclude(waveform_version=2)
            for mix in mixes:
                from PIL import Image
                import glob

                output_file = '{0}/waveforms/{1}.{2}'.format(settings.MEDIA_ROOT, mix.uid, 'png')
                if os.path.exists(output_file):
                    try:
                        print 'Processing: %s' % mix.slug
                        im = Image.open(output_file)
                        w, h = im.size
                        im.crop((0, 0, w, h / 2)).save(output_file)
                    except Exception:
                        print "Exception with image: %s" % output_file
                else:
                    print "Skipping: %s" % mix.slug
                mix.waveform_version = 2
                mix.save()
                pass
        except Exception, ex:
            print "Debug exception: %s" % ex.message