from dircache import listdir
import os
from django.core.management.base import NoArgsCommand
from os.path import isfile, join
from dss import settings
from spa.models import Mix


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        try:
            print("Starting")
            mixes_path = join(settings.MEDIA_ROOT, "mixes")
            expired_path = join(settings.MEDIA_ROOT, "mixes/expired")
            files = [f for f in listdir(mixes_path) if isfile(join(mixes_path, f))]

            for f in files:
                uid = os.path.splitext(f)[0]
                try:
                    Mix.objects.get(uid=uid)
                except Mix.DoesNotExist:
                    new_file = os.path.join(expired_path, f)
                    os.rename(os.path.join(mixes_path, f), new_file)
                    print("Moved %s to %s" % (f, new_file))
                except Exception as ex:
                    print("Error in file: %s" % ex.message)

        except Exception as ex:
            print("Error: %s" % ex.message)

