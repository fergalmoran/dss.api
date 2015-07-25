import json
import datetime
import redis
import settings

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
    print "Message sent: {0}".format(response)
