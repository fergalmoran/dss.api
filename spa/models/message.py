from datetime import datetime
from django.db import models
from django.db.models import Q
from spa.models import BaseModel, Notification


class MessageManager(models.Manager):
    def inbox_for(self, from_user, to_user):
        return self.filter(
            from_user=from_user,
            to_user=to_user
        )

    def get_chat(self, user1, user2):
        return self.filter(
            Q(from_user=user1, to_user=user2) |
            Q(from_user=user2, to_user=user1)
        )


class Message(BaseModel):
    objects = MessageManager()

    from_user = models.ForeignKey('spa.UserProfile', null=True, blank=True, related_name='sent_messages')
    to_user = models.ForeignKey('spa.UserProfile', null=True, blank=True, related_name='messages')

    sent_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)

    body = models.TextField()

    def create_notification(self, accept=False):
        try:
            notification = Notification()
            notification.from_user = self.from_user
            notification.to_user = self.to_user

            notification.verb = "Sent"
            notification.type = "Message"
            notification.target = self.id
            notification.target_desc = self.body
            notification.date = self.sent_at

            if accept:
                notification.accepted_date = datetime.now()

            notification.save()
        except Exception, ex:
            print "Error creating message notification: %s" % ex.message