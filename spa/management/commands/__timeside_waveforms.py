from django.core.management.base import NoArgsCommand
import timeside


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            audio_file = '/home/fergalm/Dropbox/Private/deepsouthsounds.com/working/sample.mp3'
            decoder = timeside.decoder.FileDecoder(audio_file)
            grapher = timeside.grapher.Spectrogram(width=1920, height=1080)
            (decoder | grapher).run()
            grapher.render('d:\spectrogram.png')

        except Exception, ex:
            print "Debug exception: %s" % ex.message