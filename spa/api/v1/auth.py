from tastypie.authorization import Authorization


class UserOwnsRowAuthorisation(Authorization):
    """
     If the user is already authenticated by a django session it will 
     allow the request (useful for ajax calls) .
     In addition, we will check that the user owns the row being updated
     or is an admin
    """

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(author__username=request.user.username)

        return object_list.none()