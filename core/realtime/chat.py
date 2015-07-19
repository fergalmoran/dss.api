import json
import datetime
import redis


def post_chat(session, image, user, message):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    payload = json.dumps({
        'session': session,
        'message': message,
        'user': user,
        'image': image,
        'date': datetime.datetime.now().isoformat()
    })
    response = r.publish('chat', payload)
    print "Message sent: {0}".format(response)
