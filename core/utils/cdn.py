import os
from azure import WindowsAzureMissingResourceError
from azure.storage import BlobService
from core.utils.url import url_path_join
from dss import settings
from dss.storagesettings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver


def upload_to_azure(in_file, filetype, uid):
    if os.path.isfile(in_file):
        print "Uploading file for: %s" % in_file
        file_name = "%s.%s" % (uid, filetype)
        archive_path = url_path_join(settings.AZURE_ITEM_BASE_URL, settings.AZURE_CONTAINER, file_name)

        cls = get_driver(Provider.AZURE_BLOBS)
        driver = cls(settings.AZURE_ACCOUNT_NAME, settings.AZURE_ACCOUNT_KEY)
        container = driver.get_container(container_name=settings.AZURE_CONTAINER)

        with open(in_file, 'rb') as iterator:
            obj = driver.upload_object_via_stream(
                iterator=iterator,
                container=container,
                object_name=file_name
            )
            print "Uploaded"
            return obj

    return None


def set_azure_details(blob_name, download_name):
    try:
        blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
        blob = blob_service.get_blob(AZURE_CONTAINER, blob_name)
        if blob:
            blob_service.set_blob_properties(
                AZURE_CONTAINER,
                blob_name,
                x_ms_blob_content_type='application/octet-stream',
                x_ms_blob_content_disposition='attachment;filename="{0}"'.format(download_name)
            )
            print "Processed: %s" % download_name
        else:
            print "No blob found for: %s" % download_name
    except WindowsAzureMissingResourceError:
        print "No blob found for: %s" % download_name
    except Exception, ex:
        print "Error processing blob %s: %s" % (download_name, ex.message)
