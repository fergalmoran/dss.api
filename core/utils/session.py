from django.contrib.sessions.models import Session
from django.utils import timezone


def get_active_sessions(session):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    if session is not None:
        sessions = sessions.filter(session_id=session.id)
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    from spa.models import UserProfile
    return UserProfile.objects.filter(user_id__in=uid_list)
