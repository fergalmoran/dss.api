import redis
import json


def post_activity(channel, session, message):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    response = r.publish(channel, json.dumps({'session': session, 'message': message}))
    print "Message sent: {0}".format(response)

if __name__ == '__main__':
    post_activity('site:broadcast', '3a596ca6c97065a67aca3dc4a3ba230d688cf413', 'bargle')

