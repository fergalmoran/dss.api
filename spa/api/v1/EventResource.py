from django.core.exceptions import ObjectDoesNotExist
import humanize
from tastypie.authorization import Authorization
from spa.api.v1.BaseResource import BaseResource
from spa.models.recurrence import Recurrence
"""
from spa.views.venue import Venue
from spa.views.event import  Event
class EventResource(BackboneCompatibleResource):
    class Meta:
        queryset = Event.objects.all()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = {'pk': request.user.pk}
        return super(EventResource, self).obj_create(bundle, request, user=request.user.get_profile())

    def dehydrate(self, bundle):
        bundle.data['item_url'] = 'event/%s' % bundle.obj.id
        bundle.data['event_venue'] = bundle.obj.event_venue.venue_name
        return bundle

    def dehydrate_event_date(self, bundle):
        return humanize.naturalday(bundle.obj.event_date)

    def hydrate(self, bundle):
        if 'event_venue' in bundle.data:
            try:
                venue = Venue.objects.get(venue_name__exact=bundle.data['event_venue'])
            except ObjectDoesNotExist:
                venue = Venue(venue_name=bundle.data['event_venue'], user=bundle.request.user)
                venue.save()

            bundle.obj.event_venue = venue

        recurrence = Recurrence.objects.get(pk=bundle.data['event_recurrence_id'])
        if recurrence != None:
            bundle.obj.event_recurrence = recurrence

        return bundle
"""
