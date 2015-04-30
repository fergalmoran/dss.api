from django.db import models
from sorl.thumbnail import get_thumbnail
from core.utils.url import unique_slugify
from dss import settings
from spa.models import BaseModel, UserProfile, Mix


class PlaylistManager(models.Manager):
    pass

    def get_by_id_or_slug(self, id_or_slug):
        try:
            return super(PlaylistManager, self).get(slug=id_or_slug)
        except Playlist.DoesNotExist:
            return super(PlaylistManager, self).get(id=id_or_slug)


class Playlist(BaseModel):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, related_name='playlists')
    mixes = models.ManyToManyField(Mix)
    public = models.BooleanField(default=True)
    slug = models.SlugField()

    objects = PlaylistManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = unique_slugify(self, self.name)

        super(Playlist, self).save(force_insert, force_update, using, update_fields)

    def get_image_url(self, size='160x160', default=''):
        if self.mixes.count() != 0:
            image = self.mixes.all()[0].get_image_url()
            try:
                ret = get_thumbnail(image, size, crop='center')
                return "%s/%s" % (settings.MEDIA_URL, ret.name)
            except Exception, ex:
                pass

        return super(Playlist, self).get_image_url(self.mix_image, settings.STATIC_URL + 'images/default-track-200.png')

    def get_absolute_url(self):
        return '/playlist/%s' % self.slug