from django.contrib import admin
from spa.models.genre import Genre
from spa.models.userprofile import UserProfile
from spa.models.chatmessage import ChatMessage
from spa.models.release import Release
from spa.models.label import Label
from spa.models.mix import Mix
from spa.models.release import ReleaseAudio
from spa.models.venue import Venue


class DefaultAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Mix)
admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Release, DefaultAdmin)
admin.site.register(ReleaseAudio)
admin.site.register(Venue)
admin.site.register(UserProfile)
admin.site.register(ChatMessage)
