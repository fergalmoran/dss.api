from spa.api.v1.BaseResource import BaseResource
from spa.models.chatmessage import ChatMessage

class ChatResource(BaseResource):
    class Meta:
        queryset = ChatMessage.objects.all().order_by('-timestamp')
        resource_name = 'chat'
