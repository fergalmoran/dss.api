import os
from django.core.management.base import NoArgsCommand
from core.utils import cdn
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            print('Enumerating items')
            items = cdn.enumerate_objects('mixes')
            for item in items:
                # Check if we have a corresponding mix
                uid, type = os.path.splitext(item)
                try:
                    Mix.objects.get(uid=uid)
                except Mix.DoesNotExist:
                    # no mix found - delete the blob
                    cdn.delete_object('mixes', item)
                    print(("Deleting blob: {0}".format(uid)))
        except Exception as ex:
            print(('Debug exception: %s' % ex.message))
