from spa.models import BaseModel, UserProfile
from django.db import models


class Blog(BaseModel):
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    date_created = models.DateField(auto_now=True)

    title = models.CharField(max_length=1024)
    body = models.TextField()
