import logging
import urllib2
from bs4 import BeautifulSoup

def _parseItem(soup, param):
    try:
        match = soup.find(text=param)
        if match is not None:
            return match.findNext('td').contents[0]
    except Exception, ex:
        logging.getLogger('core').exception("Error parsing ice stream details: " + ex.message)

    return ""


def get_server_details(server, port, mount):
    server = "http://%s:%s/status.xsl?mount=/%s" % (server, port, mount)
    print "Getting info for %s" % server
    try:
        response = urllib2.urlopen(server)
        html = response.read()
        if html:
            soup = BeautifulSoup(html)
            info = {
                'stream_title':         _parseItem(soup, "Stream Title:"),
                'stream_description':   _parseItem(soup, "Stream Description:"),
                'content_type':         _parseItem(soup, "Content Type:"),
                'mount_started':        _parseItem(soup, "Mount started:"),
                'quality':              _parseItem(soup, "Quality:"),
                'current_listeners':    _parseItem(soup, "Current Listeners:"),
                'peak_listeners':       _parseItem(soup, "Peak Listeners:"),
                'stream_genre':         _parseItem(soup, "Stream Genre:"),
                'current_song':         _parseItem(soup, "Current Song:")
            }
            return info
        else:
            print "Invalid content found"
            return None

    except urllib2.URLError:
        return "Unknown stream %s" % server

def get_now_playing(server, port, mount):
    return get_server_details(server, port, mount)
