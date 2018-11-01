from datetime import datetime, timedelta
from django.db import models
from spa.models.mix import Mix
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel
import recurrence
import recurrence.fields


class ShowOverlapException(Exception):
    pass


class Show(BaseModel):
    mix = models.ForeignKey(Mix, related_name='show', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='owned_shows', on_delete=models.CASCADE)
    performer = models.ForeignKey(UserProfile, related_name='shows', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True)
    recurrence = models.CharField(max_length=1)
    description = models.CharField(max_length=2048)

    class Meta:
        app_label = 'spa'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # throw an exception if event overlaps with another event
        if not self.end_date:
            # Default show is one hour
            self.end_date = self.start_date + timedelta(hours=1)

        overlaps = Show.objects.filter(
            models.Q(start_date__gte=self.start_date, end_date__lte=self.start_date) |
            models.Q(start_date__gte=self.end_date, end_date__lte=self.end_date)
        )
        if len(overlaps) != 0:
            raise ShowOverlapException()

        return super(Show, self).save(force_insert, force_update, using, update_fields)

    def get_recurrence_rrule(self):
        r = recurrence.Recurrence(
            dtstart=self.start_date,
            dtend=datetime(2014, 1, 3, 0, 0, 0),
            rrules=[recurrence.Rule(recurrence.WEEKLY), ]
        )
        return r
