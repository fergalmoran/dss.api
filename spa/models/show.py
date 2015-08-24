from datetime import datetime
from django.db import models
from spa.models.mix import Mix
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel
import recurrence
import recurrence.fields


class ShowOverlapException(Exception):
    pass


class Show(BaseModel):
    mix = models.ForeignKey(Mix, related_name='show')
    user = models.ForeignKey(UserProfile, related_name='show')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    recurrence = recurrence.fields.RecurrenceField()
    description = models.CharField(max_length=2048)

    class Meta:
        app_label = 'spa'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # throw an exception if event overlaps with another event

        # DEBUG
        self.start_date = datetime.now()
        self.end_date = datetime.now()
        # END DEBUG
        overlaps = Show.objects.filter(
            models.Q(start_date__gte=self.start_date, end_date__lte=self.start_date) |
            models.Q(start_date__gte=self.end_date, end_date__lte=self.end_date)
        )
        if len(overlaps) != 0:
            raise ShowOverlapException()

        self.recurrence = recurrence.Recurrence(
            dtstart=datetime(2014, 1, 2, 0, 0, 0),
            dtend=datetime(2014, 1, 3, 0, 0, 0),
            rrules=[recurrence.Rule(recurrence.WEEKLY), ]
        )

        return super(Show, self).save(force_insert, force_update, using, update_fields)
