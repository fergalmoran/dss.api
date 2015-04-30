from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from spa.api.v1.BaseResource import BaseResource
from spa.models import Genre


class GenreResource(BaseResource):
	class Meta:
		queryset = Genre.objects.all().order_by('description')
		resource_name = 'genres'

		excludes = ['resource_uri']
		filtering = {
            'slug': ('exact',),
		}
		authorization = Authorization()
		authentication = Authentication()
		always_return_data = True

	def obj_create(self, bundle, **kwargs):
		"""
			Check to see if there is an existing genre for what was entered
		"""
		genre = Genre.objects.get(description=bundle.obj['description'])
		if genre is not None:
			bundle.obj = genre
			return bundle
		else:
			ret = super(GenreResource, self).obj_create(bundle, bundle.request)

		return ret

