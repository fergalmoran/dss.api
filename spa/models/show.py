from django.db.models import Q, ForeignKey
from schedule.models import Event
from spa.models import Mix


class ShowOverlapException(Exception):
    pass


class Show(Event):
    mix = ForeignKey(Mix, related_name='show')

    class Meta:
        app_label = 'spa'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        overlaps = Show.objects.filter(
            Q(start__gte=self.start, end__lte=self.start) |
            Q(start__gte=self.end, end__lte=self.end)
        )
        if len(overlaps) != 0:
            raise ShowOverlapException()

        return super(Show, self).save(force_insert, force_update, using, update_fields)
