from django.contrib.auth.models import User
from django.db import models

from spa.models import BaseModel, UserProfile
from spa.models.mix import Mix


class Comment(BaseModel):
    class Meta:
        app_label = 'spa'

    user = models.ForeignKey(User, editable=False, null=True, blank=True)
    mix = models.ForeignKey(Mix, editable=False, null=True, blank=True, related_name='comments')
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)
    time_index = models.IntegerField(default=0)
    likes = models.ManyToManyField(UserProfile, related_name='liked_comments', blank=True)

    def get_absolute_url(self):
        return '/comment/%i' % self.id

    def create_activity(self):
        pass

    def get_user(self):
        return self.user.userprofile if self.user.is_authenticated() else self.user

    @property
    def avatar_image(self):
        if self.user is None:
            return UserProfile.get_default_avatar_image()
        else:
            return self.user.userprofile.get_avatar_image()

    @property
    def user_display_name(self):
        if self.user is None:
            return UserProfile.get_default_display_name()
        else:
            return self.user.userprofile.get_nice_name()
