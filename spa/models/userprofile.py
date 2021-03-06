import logging
import os

import urllib.parse
from bitfield.models import BitField
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.db.models import Count
import uuid
from django_gravatar.helpers import has_gravatar, get_gravatar_url
from sorl import thumbnail

from core.utils.file import generate_save_file_name
from core.utils.url import unique_slugify
from dss import settings
from spa.models.basemodel import BaseModel

logger = logging.getLogger(__name__)


def avatar_name(instance, filename):
    return generate_save_file_name(str(instance.id), 'avatars', filename)


class UserProfileManager(models.Manager):
    def get_query_set(self):
        return super(UserProfileManager, self).get_query_set().annotate(mix_count=Count('mixes'))


class UserUpdateException(Exception):
    pass


class UserProfile(BaseModel):
    class Meta:
        app_label = 'spa'

    objects = UserProfileManager()

    ACTIVITY_SHARE_NETWORK_FACEBOOK = 1
    ACTIVITY_SHARE_NETWORK_TWITTER = 2

    user = models.OneToOneField(User, unique=True, related_name='userprofile')
    uid = models.UUIDField(primary_key=False, editable=False, null=True)

    avatar_type = models.CharField(max_length=15, default='social')
    avatar_image = models.ImageField(max_length=1024, blank=True, upload_to=avatar_name)
    display_name = models.CharField(blank=True, max_length=35)
    description = models.CharField(blank=True, max_length=2048)

    slug = models.SlugField(max_length=50, blank=True, null=True, default=None)
    activity_sharing_networks = models.IntegerField(default=0)

    NOTIFICATION_CHOICES = (
        ('plays', 'Plays'),
        ('likes', 'Likes'),
        ('favourites', 'Favourites'),
        ('follows', 'Follows'),
        ('comments', 'Comments'),
    )

    activity_sharing_facebook = BitField(flags=NOTIFICATION_CHOICES, default=0)
    activity_sharing_twitter = BitField(flags=NOTIFICATION_CHOICES, default=0)
    email_notifications = BitField(flags=NOTIFICATION_CHOICES, default=0)

    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

    # location properties
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    last_known_session = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s - %s" % (self.user.get_full_name(), self.slug)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        if self.slug is None or self.slug == '':
            self.slug = unique_slugify(self, self.user.get_username())
            print("Slugified: %s" % self.slug)

        return super(UserProfile, self).save(force_insert, force_update, using, update_fields)

    def get_roles(self):
        """
        return [
            '*',
            'admin',
            'staff',
            'homepage',
            'user',
            'guest'
        ]
        """

        roles = ['guest']

        if self.user.is_superuser:
            roles.append('admin')

        if self.user.is_staff:
            roles.append('staff')

        if self.user.is_authenticated():
            roles.append('user')

        return roles

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    email = property(get_email)

    def get_first_name(self):
        return self.user.first_name

    first_name = property(get_first_name)

    def get_last_name(self):
        return self.user.last_name

    last_name = property(get_last_name)

    def __create_slug(self):
        try:
            unique_slugify(self, self.get_username() or self.user.get_full_name(), slug_separator='_')
            self.save()
        except Exception as e:
            self.logger.error("Unable to create profile slug: %s", e)

    def get_session_id(self):
        return str(self.id)

    def toggle_favourite(self, mix, value):
        try:
            if value:
                if self.activity.filter(mix=mix).count() == 0:
                    self.activity.model.add(mix=mix, user=self)
                    self.favourites.model.save()
            else:
                self.favourites.model.delete(mix=mix)
        except Exception as ex:
            self.logger.error("Exception updating favourite: %s" % ex)

    def is_follower(self, user):
        try:
            return user in self.followers.all()
        except Exception as ex:
            logger.error(ex)

        return False

    def get_absolute_url(self):
        if self.slug is None or len(self.slug) == 0:
            self.__create_slug()

        return "user/%s" % self.slug

    def get_nice_name(self):
        return self.display_name or self.first_name + ' ' + self.last_name

    def get_sized_avatar_image(self, width, height):
        try:
            #import ipdb; ipdb.set_trace()
            image = self.get_avatar_image()
            logger.debug("get_sized_avatar_image: %s".format(image))
            sized = thumbnail.get_thumbnail(image, "%sx%s" % (width, height), crop="center")
            return urllib.parse.urljoin(settings.MEDIA_URL, sized.name)
        except SuspiciousOperation:
            return UserProfile.get_default_avatar_image()
        except Exception as ex:
            return UserProfile.get_default_avatar_image()

    def get_avatar_image(self):
        avatar_type = self.avatar_type
        if avatar_type == 'gravatar':
            gravatar_exists = has_gravatar(self.email)
            if gravatar_exists:
                return get_gravatar_url(self.email)
        else:
            if os.path.exists(self.avatar_image.file.name):
                return self.avatar_image
            else:
                return self.get_default_avatar_image()

        return UserProfile.get_default_avatar_image()

    def get_profile_url(self):
        return '/user/%s' % (self.slug)

    def get_profile_description(self):
        try:
            return self.description
        except Exception as ex:
            pass

        return settings.DEFAULT_USER_TITLE

    @classmethod
    def get_default_avatar_image(cls):
        return settings.DEFAULT_USER_IMAGE

    @classmethod
    def get_default_display_name(cls):
        return settings.DEFAULT_USER_NAME

    @classmethod
    def get_user(cls, user):
        if user is not None:
            return user
        else:
            username = 'anonymous'
            u = User(username=username, first_name='Anonymous', last_name='User')
            u.set_unusable_password()

            u.username = u.id

            # comment out the next two lines if you aren't using profiles
            p = UserProfile(user=u)
            return p

    def add_following(self, user):
        from spa.models.activity import ActivityFollow
        try:
            if user is None:
                return
            if user.user.is_authenticated():
                v = ActivityFollow(user=self, to_user=user)
                v.save()
                self.following.add(user)
                self.save()
        except Exception as ex:
            self.logger.error("Exception updating like: %s" % ex)
            raise UserUpdateException(ex)

    def remove_following(self, user):
        try:
            if user is None:
                return
            if user.user.is_authenticated():
                self.following.remove(user)
                self.save()
        except Exception as ex:
            self.logger.error("Exception updating like: %s" % ex)
            raise UserUpdateException(ex)
