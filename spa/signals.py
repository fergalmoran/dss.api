from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import Signal, receiver

from django.contrib.auth.models import User

from core.utils.audio.mp3 import mp3_length
from spa.models.activity import ActivityFollow
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix


waveform_generated_signal = Signal()


def _waveform_generated_callback(sender, **kwargs):
    print "Updating model with waveform"
    try:
        uid = kwargs['uid']
        path = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.waveform_generated = True
                mix.duration = mp3_length(path)
                mix.save(update_fields=["waveform_generated", "duration"])

    except ObjectDoesNotExist:
        print "Mix has still not been uploaded"
        pass


waveform_generated_signal.connect(_waveform_generated_callback)

mix_sent_to_cdn_signal = Signal()


def _mix_sent_to_cdn_callback(sender, **kwargs):
    print "Updating model with archive bit"
    try:
        uid = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.archive_updated = True
                mix.save(update_fields=["waveform_generated", "duration"])
    except ObjectDoesNotExist:
        print "Mix has still not been uploaded"
        pass


mix_sent_to_cdn_signal.connect(_mix_sent_to_cdn_callback)

update_user_geoip_signal = Signal()


def _update_user_geoip_callback(sender, **kwargs):
    try:
        user = UserProfile.objects.get(pk=kwargs['profile_id'])
        user.city = kwargs['city']
        user.country = kwargs['country']
        user.save()
    except ObjectDoesNotExist:
        pass


update_user_geoip_signal.connect(_update_user_geoip_callback)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        up.save()


post_save.connect(create_profile, sender=User)


def post_save_handler(**kwargs):
    """
        Doing signals for notifications here.
        I like this method because I have a single signal
        and just check for a hook method on the sender
    """
    instance = kwargs['instance']
    # should save generate a notification to a target user
    if hasattr(instance, 'post_social'):
        instance.post_social()
    if hasattr(instance, 'create_notification'):
        instance.create_notification()
    # should save post to the activity feed
    if hasattr(instance, 'create_activity'):
        instance.create_activity()

    # try to get the user's geo profile
    if hasattr(instance, 'update_geo_info'):
        instance.update_geo_info()


post_save.connect(post_save_handler)

"""
    Setting up a post save handler for sessions here
    So that I can store the session id against the user
"""


@receiver(pre_save, sender=Session, dispatch_uid='session_pre_save')
def session_pre_save(sender, **kwargs):
    s = kwargs['instance']
    if s is not None:
        uid = s.get_decoded().get('_auth_user_id')
        if uid is not None:
            try:
                user = User.objects.get(pk=uid)
                p = user.get_profile()
                p.last_known_session = s.session_key
                p.save()
            except ObjectDoesNotExist:
                pass


@receiver(m2m_changed, sender=UserProfile.following.through, dispatch_uid='user_followers_changed')
def user_followers_changed(sender, **kwargs):
    print "Followers changed"

    try:
        if kwargs['action'] == 'post_add':
            source_user = kwargs['instance']
            if source_user:
                for i in kwargs['pk_set']:
                    target_user = UserProfile.objects.get(pk=i)
                    if target_user:
                        ActivityFollow(user=source_user, to_user=target_user).save()
    except Exception, ex:
        print "Error sending new follower: %s" % ex.message
