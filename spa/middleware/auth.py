from django.contrib import auth


class AuthenticationMiddleware(object):
    def process_request(self, request):
        user_cookie_name = "session_key"
        if user_cookie_name not in request.COOKIES:
            # log user out if you want
            return
        id = request.COOKIES.get(user_cookie_name)
        # this will find the right backend
        user = auth.authenticate(id)
        request.user = user
