import abc
from django.contrib.auth.models import AnonymousUser, User

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
        return "{0}".format(self.get_object_name())

    def get_user(self):
        if self.user is not None:
            return self.user
        else:
            username = 'anonymous'
            u = User(username=username, first_name='Anonymous', last_name='User')
            u.set_unusable_password()

            u.username = u.id

            # comment out the next two lines if you aren't using profiles
            p = UserProfile(user=u)
            return p

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

            # TODO: re-enable this once I figure out psa
            """
            social_account = SocialToken.objects.filter(account__user=self.user.user, account__provider='facebook')[0]
            facebook = OpenFacebook(social_account.token)
            notification_html = {
                object: wrap_full(self.get_object_url())
            }
            result = facebook.set('me/%s' % action_type, notification_html)
            print result
            """
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

            notification._activity = self
            notification.save()
        except Exception, ex:
            print "Error creating activity notification: %s" % ex.message

    def get_activity_url(self):
        return '/api/v1/activity/%s' % self.id

    @abc.abstractmethod
    def should_send_email(self):
        pass

    @abc.abstractmethod
    def get_target_user(self):
        pass

    @abc.abstractmethod
    def get_object_type(self):
        return

    @abc.abstractmethod
    def get_object_name(self):
        return

    @abc.abstractmethod
    def get_object_url(self):
        pass

    @abc.abstractmethod
    def get_object_slug(self):
        pass

    @abc.abstractmethod
    def get_object_singular(self):
        pass

    def get_object_name_for_notification(self):
        return self.get_object_name()


class ActivityFavourite(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_favourites')

    def __unicode__(self):
        return "%s - %s" % (self.mix.user.get_nice_name(), self.date)

    def get_target_user(self):
        return self.mix.user

    def get_object_type(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_slug(self):
        return self.mix.slug

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "favourited"

    def should_send_email(self):
        return self.to_user.email_notifications.favourites.is_set

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.mix.user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)


class ActivityFollow(Activity):
    to_user = models.ForeignKey('spa.UserProfile', related_name='activity_follow')

    def __unicode__(self):
        return "%s - %s" % (self.to_user.get_nice_name(), self.date)

    def get_target_user(self):
        return self.to_user

    def get_object_type(self):
        return "user"

    def get_object_name(self):
        return self.to_user.get_nice_name()

    def get_object_url(self):
        return self.to_user.get_profile_url()

    def get_object_slug(self):
        return self.to_user.slug

    def get_object_singular(self):
        return "user"

    def get_verb_past(self):
        return "followed"

    def get_object_name_for_notification(self):
        return "You"

    def should_send_email(self):
        return self.to_user.email_notifications.follows.is_set

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.to_user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)


class ActivityPlay(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_plays')

    def __unicode__(self):
        return "%s - %s" % (self.mix.user.get_nice_name(), self.date)

    def get_target_user(self):
        return self.mix.user

    def get_object_type(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_slug(self):
        return self.mix.slug

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "played"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.mix.user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)

    def should_send_email(self):
        return self.to_user.email_notifications.plays.is_set


class ActivityLike(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_likes')

    def __unicode__(self):
        return "%s - %s" % (self.mix.user.get_nice_name(), self.date)

    def get_target_user(self):
        return self.mix.user

    def get_object_type(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_slug(self):
        return self.mix.slug

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "liked"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.mix.user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)


class ActivityDownload(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_downloads')

    def get_target_user(self):
        return self.mix.user

    def get_object_type(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_slug(self):
        return self.mix.slug

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "downloaded"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.mix.user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)


class ActivityComment(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_comments')

    def get_target_user(self):
        return self.mix.user

    def get_object_type(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_slug(self):
        return self.mix.slug

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "commented on"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__to_user = self.mix.user
        return super(Activity, self).save(force_insert, force_update, using, update_fields)
