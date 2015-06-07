import abc
from django.contrib.auth.models import AnonymousUser, User

from allauth.socialaccount.models import SocialToken
from datetime import datetime
from django.db import models
from model_utils.managers import InheritanceManager

from open_facebook import OpenFacebook

from core.utils.url import wrap_full
from dss import settings
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel


ACTIVITYTYPES = (
    ('p', 'played'),
    ('d', 'downloaded'),
    ('l', 'liked'),
    ('f', 'favourited'),
    ('l', 'followed')
)


class Activity(BaseModel):
    objects = InheritanceManager()
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.get_object_name()

    def get_user(self):
        return UserProfile.get_user(self.user)

    def post_social(self):
        if settings.DEBUG:
            return

        try:
            verb = self.get_verb_past()
            object = self.get_object_singular()
            if verb == "favourited":
                action_type = "deepsouthsounds:favourite"
            if verb == "liked":
                action_type = "like"
            if verb == "followed":
                action_type = "og.follows"
            else:
                action_type = "deepsouthsounds:play"

            social_account = SocialToken.objects.filter(account__user=self.user.user, account__provider='facebook')[0]
            facebook = OpenFacebook(social_account.token)
            notification_html = {
                object: wrap_full(self.get_object_url())
            }
            result = facebook.set('me/%s' % action_type, notification_html)
            print result
        except Exception, ex:
            print ex.message
            pass

    def create_notification(self):
        try:
            notification = Notification()
            notification.from_user = self.user
            notification.to_user = self.get_target_user()
            notification.notification_text = "%s %s %s" % (
                self.user.get_nice_name() if self.user is not None else "Anonymouse",
                self.get_verb_past(),
                self.get_object_name_for_notification())

            notification.notification_html = "<a href='%s'>%s</a> %s <a href='%s'>%s</a>" % (
                wrap_full(self.user.get_profile_url() if self.user is not None else ""),
                self.user.get_nice_name() if self.user is not None else "Anonymouse",
                self.get_verb_past(),
                wrap_full(self.get_object_url()),
                self.get_object_name_for_notification()
            )

            notification.notification_url = self.get_object_url()
            notification.verb = self.get_verb_past()
            notification.target = self.get_object_name()
            notification.save()
        except Exception, ex:
            print "Error creating activity notification: %s" % ex.message

    def get_activity_url(self):
        return '/api/v1/activity/%s' % self.id

    @abc.abstractmethod
    def get_object_type(self):
        return

    @abc.abstractmethod
    def get_object_slug(self):
        pass

    @abc.abstractmethod
    def get_target_user(self):
        pass

    @abc.abstractmethod
    def get_object_name(self):
        pass

    @abc.abstractmethod
    def get_object_url(self):
        pass

    @abc.abstractmethod
    def get_object_singular(self):
        pass

    def get_object_name_for_notification(self):
        return self.get_object_name()


class ActivityLike(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_likes')

    class Meta:
        app_label = 'spa'

    def get_object_type(self):
        return "mix"

    def get_object_slug(self):
        return self.mix.slug

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "liked"


class ActivityFollow(Activity):
    to_user = models.ForeignKey('spa.UserProfile', related_name='activity_follow')

    def get_object_type(self):
        return "user"

    def get_object_slug(self):
        return self.to_user.slug

    def get_target_user(self):
        return self.to_user

    def get_object_name(self):
        return self.to_user.get_nice_name()

    def get_object_url(self):
        return self.to_user.get_profile_url()

    def get_object_singular(self):
        return "user"

    def get_verb_past(self):
        return "followed"

    def get_object_name_for_notification(self):
        return "You"


class ActivityFavourite(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_favourites')

    def get_object_type(self):
        return "mix"

    def get_object_slug(self):
        return self.mix.slug

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "favourited"


class ActivityPlay(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_plays')

    def get_object_type(self):
        return "mix"

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "played"


class ActivityDownload(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_downloads')

    def get_object_type(self):
        return "mix"

    def get_object_slug(self):
        return self.mix.slug

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "downloaded"


class ActivityComment(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_comments')

    def get_object_type(self):
        return "mix"

    def get_object_slug(self):
        return self.mix.slug

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "commented on"