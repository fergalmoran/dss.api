from tastypie import fields
from spa.api.v1.BaseResource import BaseResource
from spa.models.release import ReleaseAudio

class ReleaseAudioResource(BaseResource):
    release = fields.ToOneField('spa.api.v1.ReleaseResource.ReleaseResource', 'release')

    class Meta:
        queryset = ReleaseAudio.objects.all()
        resource_name = 'audio'
        filtering = {
            "release": ('exact',),
            }

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        return bundle