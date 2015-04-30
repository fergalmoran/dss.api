from django.db.models import Count
from tastypie import fields
from tastypie.resources import ModelResource
from spa.models import UserProfile


class DebugResource(ModelResource):
    total_tickets = fields.IntegerField(readonly=True)

    class Meta:
        queryset = UserProfile.objects.all()
        ordering = ['total_tickets']

    def get_object_list(self, request):
        return super(DebugResource, self).get_object_list(request).annotate(total_tickets=Count('mixes', distinct=True))

    def dehydrate_total_tickets(self, bundle):
        return bundle.obj.total_tickets