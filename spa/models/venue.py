from django.contrib.auth.models import User
from django.db import models
from core.utils.file import generate_save_file_name
from spa.models.basemodel import BaseModel

def venue_image_name(instance, filename):
    return generate_save_file_name('venue-images', filename)

class Venue(BaseModel):
    class Meta:
        app_label = 'spa'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=250)
    venue_address = models.CharField(max_length=1024)
    venue_image = models.ImageField(blank=True, upload_to=venue_image_name)

    def __unicode__(self):
        return self.venue_name

    @classmethod
    def get_select_lookup(cls):
        return {'name' :'venue_name'}
