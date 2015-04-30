from django.core.management.base import NoArgsCommand, CommandError
from django.template.defaultfilters import slugify
from core.utils.audio import Mp3FileNotFoundException
from core.utils.audio.mp3 import mp3_length
from core.utils.url import unique_slugify
from spa.models import Mix


class Command(NoArgsCommand):
    help = "Updates audio files with their durations"

    def handle(self, *args, **options):
        try:
            candidates = Mix.objects.all()
            for mix in candidates:
                try:
                    if mix.duration is None:
                        print "Finding duration for: %s" % mix.title
                        length = mp3_length(mix.get_absolute_path())
                        print "\tLength: %d" % length
                        mix.duration = length
                    if mix.slug == 'Invalid':
                        print "Slugifying mix: %s" % mix.title
                        mix.slug = unique_slugify(mix, mix.title)
                        print "\tNew title: %s" % mix.slug
                    mix.save()
                except Mp3FileNotFoundException, me:
                    mix.delete()
                    print me.message
        except Exception, ex:
            raise CommandError(ex.message)
