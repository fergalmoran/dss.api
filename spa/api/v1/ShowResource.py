from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest

from spa.api.v1.BaseResource import BaseResource

from spa.models import Show
from spa.models.show import ShowOverlapException

DATE_FORMAT = '%d/%m/%Y %H:%M:%S'


class ShowResource(BaseResource):
    mix = fields.ToOneField('spa.api.v1.MixResource.MixResource',
                            'mix', null=False, full=False)

    class Meta:
        queryset = Show.objects.all()
        authorization = Authorization()
        resource_name = 'shows'

    def obj_create(self, bundle, **kwargs):
        try:
            return super(ShowResource, self).obj_create(bundle, **kwargs)
        except ShowOverlapException:
            raise ImmediateHttpResponse(
                HttpBadRequest("This event overlaps with an existing event")
            )
        except Exception, ex:
            raise ImmediateHttpResponse(
                HttpBadRequest(ex.message)
            )

