from django.db import models
from spa.models import BaseModel, UserProfile


class Session(BaseModel):
    jwt_token = models.CharField(max_length=2048)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
