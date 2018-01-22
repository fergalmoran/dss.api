from django.core.management.base import NoArgsCommand
from spa.models import Mix


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        candidates = Mix.objects.filter(waveform_generated=False)
        for mix in candidates:
            print("Deleting: %s" % mix.title)
            mix.delete()
