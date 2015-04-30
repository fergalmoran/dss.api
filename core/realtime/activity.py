import requests
from core.serialisers import json
from dss import localsettings, settings


def post_activity(session_id, activity_url):
    payload = {
        'sessionid': session_id,
        'message': activity_url
    }
    data = json.dumps(payload)
    r = requests.post(localsettings.REALTIME_HOST + 'activity', data=data, headers=settings.REALTIME_HEADERS)
    if r.status_code == 200:
        return ""
    else:
        return r.text
