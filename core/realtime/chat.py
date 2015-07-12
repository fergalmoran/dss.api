import json
import redis


def post_chat(session, message):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    response = r.publish('chat', json.dumps({'session': session, 'message': message}))
    print "Message sent: {0}".format(response)
