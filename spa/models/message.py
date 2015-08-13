from django.db import models
from spa.models import BaseModel


class Message(BaseModel):
    from_user = models.ForeignKey('spa.UserProfile', related_name='notifications', null=True, blank=True)
    to_user = models.ForeignKey('spa.UserProfile', related_name='notifications', null=True, blank=True)

    sent_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)

    body = models.TextField()
