<<<<<<< HEAD
=======
from django.db import models
>>>>>>> master
from django.db.models import Q, ForeignKey
# from schedule.models import Event
from spa.models.mix import Mix
from spa.models.basemodel import BaseModel


class ShowOverlapException(Exception):
    pass


class Show(BaseModel):  # Event):
    mix = ForeignKey(Mix, related_name='show')
    test_field = models.CharField(max_length=400)

    class Meta:
        app_label = 'spa'

<<<<<<< HEAD
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

=======
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # throw an exception if event overlaps with another event
>>>>>>> master
        overlaps = Show.objects.filter(
            Q(start__gte=self.start, end__lte=self.start) |
            Q(start__gte=self.end, end__lte=self.end)
        )
        if len(overlaps) != 0:
            raise ShowOverlapException()

        return super(Show, self).save(force_insert, force_update, using, update_fields)
