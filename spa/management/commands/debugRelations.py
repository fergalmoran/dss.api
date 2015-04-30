from django.core.management.base import NoArgsCommand
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            #l = Mix.objects.filter(slug='dss-on-deepvibes-radio-17th-july-jamie-o-sullivan')[0]
            l = Mix.objects.filter(favourites__slug='fergalmoran')[0]
            for fav in l.favourites.all():
                print fav.slug
            pass
        except Exception, ex:
            print "Debug exception: %s" % ex.message