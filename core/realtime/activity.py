import redis
import json
from dss import settings


def post_activity(channel, session, message):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
    response = r.publish(channel, json.dumps({'session': session, 'message': message}))
    print "Message sent: {0}".format(response)

if __name__ == '__main__':
    post_activity('site:broadcast', '3a596ca6c97065a67aca3dc4a3ba230d688cf413', 'bargle')

