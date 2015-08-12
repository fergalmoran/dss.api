from django.conf import settings
import mandrill
from django.db import models
from django.template import loader, Context

from core.realtime.notification import post_notification
from dss import localsettings
from spa.models import BaseModel, UserProfile


class Notification(BaseModel):
    to_user = models.ForeignKey('spa.UserProfile', related_name='to_notications')
    from_user = models.ForeignKey('spa.UserProfile', related_name='notifications', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    notification_text = models.CharField(max_length=1024)
    notification_html = models.CharField(max_length=1024)
    notification_url = models.URLField(null=True)

    verb = models.CharField(max_length=200, null=True)
    target = models.CharField(max_length=200, null=True)

    accepted_date = models.DateTimeField(null=True)

    class Meta:
        app_label = 'spa'
        ordering = ('-id',)

    def get_notification_url(self):
        return '/api/v1/notification/%s' % self.id

    def __save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self._activity.should_send_email():
            self.send_notification_email()

        sessions = self.to_user.user.session_set.all()
        avatar_image = UserProfile.get_default_avatar_image()
        if self.from_user is not None:
            avatar_image = self.from_user.get_avatar_image()

        for session in sessions:
            post_notification(
                session.session_key,
                avatar_image,
                self.notification_html)

        return super(Notification, self).save(force_insert, force_update, using, update_fields)

    def send_notification_email(self):
        try:
            if settings.DEBUG:
                return

            t = loader.get_template('email/notification/new.html')
            c = Context({
                'user_name': self.to_user.get_nice_name(),
                'notification_html': self.notification_html,
                'title': self.notification_html
            })
            rendered = t.render(c)

            mandrill_client = mandrill.Mandrill(localsettings.MANDRILL_API_KEY)
            message = {
                'inline_css': True,
                'from_email': 'chatbot@deepsouthsounds.com',
                'from_name': 'DSS ChatBot',
                'headers': {'Reply-To': 'chatbot@deepsouthsounds.com'},
                'metadata': {'website': 'www.deepsouthsounds.com'},
                'subject': self.notification_text,
                'to': [{'email': 'fergal.moran@gmail.com' if settings.DEBUG else self.to_user.email,
                        'name': self.to_user.get_nice_name(),
                        'type': 'to'}],
                'html': rendered,
                'text': 'Get yourself some HTML man!',
            }

            result = mandrill_client.messages.send(message=message, async=False)
            print result

        except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)

    def get_from_user(self):
        return UserProfile.get_user(self.from_user)
