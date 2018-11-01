from core.utils.url import unique_slugify
from spa.models import BaseModel, UserProfile
from django.db import models


class Blog(BaseModel):
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField()

    title = models.CharField(max_length=1024)
    body = models.TextField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = unique_slugify(self, self.title)

        super(Blog, self).save(force_insert, force_update, using, update_fields)


class BlogComment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    date_created = models.DateField(auto_now_add=True)
