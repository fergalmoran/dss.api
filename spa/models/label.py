from django.db import models
from spa.models.basemodel import BaseModel

class Label(BaseModel):
    class Meta:
        app_label = 'spa'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name