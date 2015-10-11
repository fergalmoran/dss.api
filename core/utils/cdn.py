from azure.common import AzureMissingResourceHttpError
from azure.storage.blob import BlobService

from dss import settings
from dss.storagesettings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER


def upload_file_to_azure(in_file, file_name, container_name=settings.AZURE_CONTAINER):
    try:
        blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
        blob_service.put_block_blob_from_path(
            container_name=container_name,
            blob_name=file_name,
            file_path=in_file,
            x_ms_blob_content_type='application/octet-stream'
        )
    except Exception as ex:
        print("Failed to upload blob: {0}".format(ex))


def set_azure_details(blob_name, download_name, container_name=AZURE_CONTAINER):
    try:
        blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
        blob = blob_service.get_blob(container_name, blob_name)
        if blob:
            blob_service.set_blob_properties(
                container_name,
                blob_name,
                x_ms_blob_content_type='application/octet-stream',
                x_ms_blob_content_disposition='attachment;filename="{0}"'.format(download_name)
            )
            print("Processed: %s" % download_name)
        else:
            print("No blob found for: %s" % download_name)
    except AzureMissingResourceHttpError:
        print("No blob found for: %s" % download_name)
    except Exception as ex:
        print("Error processing blob %s: %s" % (download_name, ex))


def file_exists(url):
    import http.client
    from urllib.parse import urlparse
    p = urlparse(url)
    c = http.client.HTTPConnection(p.netloc)
    c.request("HEAD", p.path)

    r = c.getresponse()
    return r.status == 200


def enumerate_objects(container):
    blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
    blobs = blob_service.list_blobs(container)
    items = []
    for blob in blobs:
        items.append(blob.name)

    return items


def delete_object(container, name):
    blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
    blob_service.delete_blob(container, name)