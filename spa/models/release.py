from datetime import datetime
from django.db import models
from core.utils.file import generate_save_file_name
from dss import settings
from spa.models.label import Label
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel

def release_image_name(instance, filename):
    return generate_save_file_name('release-images', filename)

def release_file_name(instance, filename):
    return generate_save_file_name('release-audio', filename)

class Release(BaseModel):
    class Meta:
        app_label = 'spa'

    release_artist = models.CharField(max_length=100)
    release_title = models.CharField(max_length=100)
    release_description = models.TextField()
    release_image = models.ImageField(blank=True, upload_to=release_image_name)
    release_label = models.ForeignKey(Label, on_delete=models.CASCADE)
    release_date = models.DateField(auto_now=True)

    embed_code = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.release_title

    def save(self, force_insert=False, force_update=False, using=None):
        self.clean_image('release_image', Release)
        super(Release, self).save(force_insert, force_update, using)

    def get_absolute_url(self):
        return '/release/%i' % self.id

    def get_image_url(self):
        return super(Release, self).get_image_url(self.release_image, "")

    @classmethod
    def get_view_model(cls):
        qs = cls.objects.get(is_active=True)
        return qs


class ReleaseAudio(BaseModel):
    class Meta:
        app_label = 'spa'

    def __unicode__(self):
        return self.description

    def get_waveform_url(self):
        return settings.MEDIA_URL + 'waveforms/release/%d.%s' % (self.id, "png")

    release = models.ForeignKey(Release, related_name='release_audio', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()