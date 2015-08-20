from django.conf import settings
from django.core.urlresolvers import reverse

class SWFUploadMiddleware(object):
    def process_request(self, request):
        if (request.method == 'POST') and\
           (request.path == reverse('jfu_upload')) and\
           settings.SESSION_COOKIE_NAME in request.POST:
            request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]