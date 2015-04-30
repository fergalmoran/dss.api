from django.core.management.base import NoArgsCommand
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from core.utils.url import url_path_join
from dss import settings
from spa.models.mix import Mix
from datetime import datetime, timedelta
from django.db.models import Count
import os
import urlparse
from os.path import isfile, join, basename


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            cls = get_driver(Provider.AZURE_BLOBS)
            driver = cls(settings.AZURE_ACCOUNT_NAME, settings.AZURE_ACCOUNT_KEY)
            container = driver.get_container(container_name=settings.AZURE_CONTAINER)

            #.filter(upload_date__lte=datetime.today() - timedelta(days=180)) \
            mixes = Mix.objects \
                .exclude(archive_path__isnull=False) \
                .annotate(num_plays=Count('activity_plays')) \
                .order_by('num_plays')
            for mix in mixes:
                if os.path.isfile(mix.get_absolute_path()):
                    print "Uploading file for: %s" % mix.slug
                    file_name = "%s.%s" % (mix.uid, mix.filetype)
                    archive_path = url_path_join(settings.AZURE_ITEM_BASE_URL, settings.AZURE_CONTAINER, file_name)

                    with open(mix.get_absolute_path(), 'rb') as iterator:
                        obj = driver.upload_object_via_stream(
                            iterator=iterator,
                            container=container,
                            object_name=file_name
                        )
                        print "Uploaded"
                        mix.archive_path = archive_path
                        mix.save()

                        expired_path = join(settings.MEDIA_ROOT, "mixes/archived")
                        new_file = os.path.join(expired_path, basename(iterator.name))
                        os.rename(iterator.name, new_file)

                    print "done- file is %s" % mix.archive_path

        except Exception, ex:
            print "Debug exception: %s" % ex.message
