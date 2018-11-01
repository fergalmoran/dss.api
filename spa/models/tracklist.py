from spa.models.mix import Mix
from spa.models.basemodel import BaseModel
from django.db import models

class Tracklist(BaseModel):
    mix = models.ForeignKey(Mix, related_name='tracklist', on_delete=models.CASCADE)
    index = models.SmallIntegerField()
    timeindex = models.TimeField(null=True)
    description = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    remixer = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
