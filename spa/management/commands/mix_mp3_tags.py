from django.core.management.base import NoArgsCommand

from core.utils.audio.mp3 import mp3_length
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            mix = Mix.objects.get(duration=None)
            if mix is not None:
                mix.waveform_generated = True
                mix.duration = mp3_length(path)
                mix.save(update_fields=["waveform_generated", "duration"])
        except Exception as ex:
            print("Debug exception: %s" % ex)