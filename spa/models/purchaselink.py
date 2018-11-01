from spa.models.basemodel import BaseModel
from spa.models.tracklist import Tracklist

from django.db import models

class PurchaseLink(BaseModel):
    track = models.ForeignKey(Tracklist, related_name='purchase_link', on_delete=models.CASCADE)
    url = models.URLField()
    provider = models.CharField(max_length=255)