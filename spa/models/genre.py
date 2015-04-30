from django.db import models
from core.utils.url import unique_slugify
from spa.models.basemodel import BaseModel


class Genre(BaseModel):
    class Meta:
        app_label = 'spa'

    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug:
            self.slug = unique_slugify(self, self.description, slug_separator='_')

        super(Genre, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.description