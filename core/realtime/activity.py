import logging
import redis
import json
from dss import settings

logger = logging.getLogger('dss')


def post_activity(channel, message, session=''):
    try:
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        payload = json.dumps({'session': session, 'message': message})
        response = r.publish(channel, payload)
        logger.debug("Message sent: {0}".format(payload))
    except Exception as ex:
        logger.error(ex)

if __name__ == '__main__':
    post_activity('site:broadcast', 'bargle', '3a596ca6c97065a67aca3dc4a3ba230d688cf413')

