import os
from django.utils.encoding import smart_str
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.db import models
from sorl.thumbnail.engines.pil_engine import Engine

from core.utils import url
from core.utils.audio import Mp3FileNotFoundException
from core.utils.audio.mp3 import mp3_length, tag_mp3
from core.utils.url import unique_slugify, url_path_join
from spa.models.activity import ActivityDownload, ActivityPlay, ActivityFavourite, \
    ActivityLike  # , ActivityTestConcrete
from spa.models.genre import Genre
from dss import settings, localsettings
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel
from core.utils.file import generate_save_file_name
from core.utils import cdn


class Engine(Engine):
    def create(self, image, geometry, options):
        thumb = super(Engine, self)
        if options.get('splice'):
            w, h = thumb.size
            thumb.crop((0, 0, w, h / 2))
            return thumb


def mix_file_name(instance, filename):
    return generate_save_file_name(instance.uid, 'mixes', filename)


def mix_image_name(instance, filename):
    ret = generate_save_file_name(instance.uid, 'mix-images', filename)
    return ret


class MixManager(models.Manager):
    pass

    def get_by_id_or_slug(self, id_or_slug):
        """
            Tries to get a mix using the slug first
            If this fails then try getting by id
        """
        try:
            return super(MixManager, self).get(slug=id_or_slug)
        except Mix.DoesNotExist:
            return super(MixManager, self).get(id=id_or_slug)


class MixUpdateException(Exception):
    pass


class Mix(BaseModel):
    class Meta:
        app_label = 'spa'
        ordering = ('-id',)
        permissions = (
            ("mix_add_homepage", "Can add a mix to the homepage"),
            ("mix_allow_download", "Can allow downloads on a mix"),
        )

    objects = MixManager()

    title = models.CharField(max_length=150)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    mix_image = models.ImageField(max_length=1024, blank=True, upload_to=mix_image_name)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_downloadable = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, related_name='mixes')
    waveform_generated = models.BooleanField(default=False)
    waveform_version = models.IntegerField(default=1)
    mp3tags_updated = models.BooleanField(default=False)
    uid = models.CharField(max_length=38, blank=True, unique=True)
    filetype = models.CharField(max_length=10, blank=False, default="mp3")
    duration = models.IntegerField(null=True, blank=True)
    archive_path = models.CharField(max_length=2048, null=True, blank=True)
    archive_updated = models.BooleanField(default=False)
    # archive_details_updated = models.BooleanField(default=False)
    slug = models.SlugField()

    genres = models.ManyToManyField(Genre)

    # activity based stuff
    favourites = models.ManyToManyField(UserProfile, related_name='favourites', blank=True)
    likes = models.ManyToManyField(UserProfile, related_name='likes', blank=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "{} - {}".format(self.user.get_nice_name(), self.title)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = unique_slugify(self, self.title)

        self.clean_image('mix_image', Mix)
        super(Mix, self).save(force_insert, force_update, using, update_fields)

    def set_cdn_details(self, path):
        self.waveform_generated = True
        self.duration = mp3_length(path)
        self.save(update_fields=["waveform_generated", "duration"])
        self.update_file_http_headers(self.uid, self.title)

    def create_mp3_tags(self, prefix=""):
        try:
            tag_mp3(
                    self.get_absolute_path(),
                    artist=self.user.get_nice_name(),
                    title=self.title,
                    url=self.get_full_url(),
                    album="Deep South Sounds Mixes",
                    year=self.upload_date.year,
                    comment=self.description,
                    genres=self.get_nice_genres())
        except Exception as ex:
            self.logger.exception("Mix: error creating tags: %s" % ex)
            pass

        return '%s/mixes/%s%s.%s' % (settings.MEDIA_ROOT, prefix, self.uid, self.filetype)

    def get_nice_genres(self):
        return ", ".join(list(self.genres.all().values_list("description", flat=True)))

    def get_cache_path(self, prefix=""):
        return '%s/mixes/%s%s.%s' % (settings.CACHE_ROOT, prefix, self.uid, self.filetype)

    def get_absolute_path(self, prefix=""):
        return '%s/mixes/%s%s.%s' % (settings.MEDIA_ROOT, prefix, self.uid, self.filetype)

    def get_absolute_url(self):
        return '/%s/%s' % (self.user.slug, self.slug)

    def get_full_url(self):
        return 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_download_url(self):
        return self.get_stream_url()  # 'HTTP://%s/audio/download/%s' % (Site.objects.get_current().domain, self.pk)

    def get_waveform_path(self):
        return os.path.join(settings.MEDIA_ROOT, "waveforms/", "%s.%s" % (self.uid, "png"))

    def get_waveform_url(self, waveform_type=""):
        # TODO: Design better flow for this sort of thing
        if not self.waveform_generated and cdn.file_exists('{0}{1}.png'.format(settings.WAVEFORM_URL, self.uid)):
            self.waveform_generated = True
            self.save()

        if self.waveform_generated:
            waveform_root = settings.WAVEFORM_URL \
                if hasattr(settings, 'WAVEFORM_URL') else "%swaveforms" % settings.MEDIA_URL

            ret = "%s/%s%s.%s" % (waveform_root, self.uid, waveform_type, "png")
            return url.urlclean(ret)
        else:
            return settings.DEFAULT_WAVEFORM_GENERATING

    def get_waveform_progress_url(self):
        return self.get_waveform_url(waveform_type="_progress")

    def get_image_url(self, size='200x200', default=''):
        try:
            if self.mix_image.name and self.mix_image.storage.exists(self.mix_image.name):
                ret = get_thumbnail(self.mix_image, size, crop='center')
                return url.urlclean("%s/%s" % (settings.MEDIA_URL, ret.name))
            else:
                return self.user.get_sized_avatar_image(253, 157)
        except Exception as ex:
            pass

        return super(Mix, self).get_image_url(self.mix_image, settings.DEFAULT_TRACK_IMAGE)

    def get_stream_url(self):
        if self.archive_path in [None, '']:
            ret = url_path_join(settings.STREAM_URL, "{0}.{1}".format(self.uid, self.filetype))
        else:
            return "{0}{1}.{2}".format(settings.AUDIO_URL, self.uid, self.filetype)
        return ret

    def get_cdn_details(self):
        blob_name = "%s.%s" % (self.uid, self.filetype)
        download_name = smart_str('{0} - {1}.{2}'.format(settings.SITE_NAME, self.title, self.filetype))
        return blob_name, download_name

    @classmethod
    def get_for_username(cls, user, queryset=None):
        if queryset is None:
            queryset = Mix.objects

        return queryset \
            .filter(user__slug__exact=user) \
            .filter(waveform_generated=True) \
            .order_by('-id')

    def add_download(self, user):
        try:
            if user.is_authenticated():
                ActivityDownload(user=user, mix=self).save()
        except Exception as e:
            self.logger.exception("Error adding mix download: %s" % e)

    def add_genre(self, new_genre):
        # first look for genre by slug
        genre = Genre.objects.get(slug=new_genre['slug'])
        if not genre:
            # need to find a genre by description
            genre = Genre.objects.get(description__iexact=new_genre['description'])
            if not genre:
                genre = Genre(description=new_genre['description'])

        if genre:
            self.genres.add(genre)
            self.save()

    def add_play(self, user):
        try:
            if user.is_authenticated():
                ActivityPlay(user=user.userprofile, mix=self).save()
            else:
                ActivityPlay(user=None, mix=self).save()

        except Exception as e:
            self.logger.exception("Unable to add mix play: %s" % e)

    def update_favourite(self, user, value):
        try:
            if user is None:
                return
            if user.user.is_authenticated():
                if value:
                    if self.favourites.filter(user=user.user).count() == 0:
                        fav = ActivityFavourite(user=user, mix=self)
                        fav.save()
                        self.favourites.add(user)
                        self.save()
                else:
                    self.favourites.remove(user)
                self.save()

        except Exception as ex:
            self.logger.error("Exception updating favourite: %s" % ex)

    def update_liked(self, user, value):
        try:
            if user is None:
                return
            if user.user.is_authenticated():
                if value:
                    if self.likes.filter(user=user.user).count() == 0:
                        v = ActivityLike(user=user, mix=self)
                        v.save()
                        self.likes.add(user)
                        self.save()
                else:
                    self.likes.remove(user)
                self.save()
        except Exception as ex:
            self.logger.error("Exception updating like: %s" % ex)
            raise MixUpdateException(ex)

    def is_favourited(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.favourites.filter(user=user).count() != 0
        else:
            return False

    def is_liked(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.likes.filter(user=user).count() != 0

        return False
