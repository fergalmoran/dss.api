from django.db import models
from .basemodel import BaseModel


class _Lookup(BaseModel):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description

    @classmethod
    def get_select_lookup(cls):
        return {'description' : 'description'}