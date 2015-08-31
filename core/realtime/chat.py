import json
import datetime
import redis
from dss import settings
import logging

logger = logging.getLogger('dss')


def post_chat(session, image, user, message):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
    payload = json.dumps({
        'session': session,
        'message': message,
        'user': user,
        'image': image,
        'date': datetime.datetime.now().isoformat()
    })
    response = r.publish('chat', payload)
    logger.debug("Message sent: {0}".format(payload))
