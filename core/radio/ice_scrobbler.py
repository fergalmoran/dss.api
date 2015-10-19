import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.connection import ConnectionError
from dss import settings


def get_server_details():
    url = "http://%s:%s/status.xsl?mount=/%s" % (settings.ICE_HOST, settings.ICE_PORT, settings.ICE_MOUNT)
    print("Getting info for %s" % url)
    try:
        response = requests.get(url)
        html = response.text
        if html:
            try:
                soup = BeautifulSoup(html, "html.parser")
                info = {
                    'stream_title': soup.find(text="Stream Title:").findNext('td').contents[0],
                    'stream_description': soup.find(text="Stream Description:").findNext('td').contents[0],
                    'content_type': soup.find(text="Content Type:").findNext('td').contents[0],
                    'mount_started': soup.find(text="Mount started:").findNext('td').contents[0],
                    'current_listeners': soup.find(text="Current Listeners:").findNext('td').contents[0],
                    'peak_listeners': soup.find(text="Peak Listeners:").findNext('td').contents[0],
                    'stream_url': soup.find(text="Stream URL:").findNext('td').findNext('a').contents[0],
                    'current_song': soup.find(text="Current Song:").findNext('td').contents[0]
                }
                return {
                    'status': 2,
                    'metadata': info
                }
            except AttributeError:
                return {
                    'status': 1
                }
        else:
            return {
                'status': 0
            }
    except Exception as ex:
        return {
            'status': 0
        }


def shuffle():
    url = "http://{}:{}/a/shuffle".format(settings.RADIO_HOST, settings.RADIO_PORT)
    r = requests.post(url)

def play(item):
    url = "http://{}:{}/a/play".format(settings.RADIO_HOST, settings.RADIO_PORT)
    r = requests.post(url, data=item)

if __name__ == '__main__':
    d = get_server_details("localhost", "8000", "dss")
    print(d)
