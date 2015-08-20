from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            pass
        except Exception as ex:
            print("Debug exception: %s" % ex)