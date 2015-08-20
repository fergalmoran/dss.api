from django.core.management.base import NoArgsCommand
from spa import models


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            models.Notification.objects.all().delete()
            act = models.Activity.objects.all().order_by('-id').select_subclasses()
            for a in act:
                print("Creating for: {0}".format(a))
                a.create_notification(accept=True)

        except Exception as ex:
            print("Debug exception: %s" % ex.message)