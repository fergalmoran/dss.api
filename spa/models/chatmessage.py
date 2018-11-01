from django.db import models
from spa.models.basemodel import BaseModel
from spa.models.userprofile import UserProfile


class ChatMessage(BaseModel):
    message = models.TextField('Message')
    timestamp = models.DateTimeField('Timestamp', auto_now_add=True)
    user = models.ForeignKey(UserProfile, related_name='chat_messages', blank=True, null=True, on_delete=models.CASCADE)
