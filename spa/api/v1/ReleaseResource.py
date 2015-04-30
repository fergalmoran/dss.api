import datetime
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BaseResource import BaseResource
from spa.models import Label
from spa.models.release import Release
from django.core.exceptions import ObjectDoesNotExist
class ReleaseResource(BaseResource):
    release_audio = fields.ToManyField('spa.api.v1.ReleaseAudioResource.ReleaseAudioResource', 'release_audio', 'release', null=True, blank=True)
    class Meta:
        queryset = Release.objects.all()
        filtering = {
            'release_audio' : ALL_WITH_RELATIONS
        }
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = {'pk': request.user.pk}
        return super(ReleaseResource, self).obj_create(bundle, request, user=request.user.get_profile())

    def hydrate(self, bundle):
        if 'release_label' in bundle.data:
            try:
                label = Label.objects.get(name__exact=bundle.data['release_label'])
            except ObjectDoesNotExist:
                label = Label(name=bundle.data['release_label'])
                label.save()

            bundle.obj.release_label = label
        return bundle

    def dehydrate(self, bundle):
        bundle.data['release_label'] = bundle.obj.release_label.name
        bundle.data['item_url'] = 'release/%s' % bundle.obj.id
        bundle.data['mode'] = 'release'
        return bundle

    def dehydrate_release_image(self, bundle):
        return bundle.obj.get_image_url()

