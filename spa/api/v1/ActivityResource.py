import humanize
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from spa.api.v1.BaseResource import BaseResource
from spa.models import UserProfile
from spa.models.activity import Activity


class ActivityResource(BaseResource):
    class Meta:
        queryset = Activity.objects.select_subclasses().order_by('-id')
        resource_name = 'activity'
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

    def dehydrate(self, bundle):
        try:
            if bundle.obj.user is not None:
                user_name = bundle.obj.user.get_nice_name()
                user_image = bundle.obj.user.get_small_profile_image()
                user_profile = bundle.obj.user.get_profile_url()
            else:
                user_name = UserProfile.get_default_display_name()
                user_image = UserProfile.get_default_avatar_image()
                user_profile = ""

            bundle.data["verb"] = bundle.obj.get_verb_past(),
            bundle.data["object"] = bundle.obj.get_object_singular(),
            bundle.data["item_name"] = bundle.obj.get_object_name(),
            bundle.data["item_url"] = bundle.obj.get_object_url(),
            bundle.data["user_name"] = user_name,
            bundle.data["user_profile"] = user_profile,
            bundle.data["user_image"] = user_image
            return bundle

        except AttributeError, ae:
            self.logger.debug("AttributeError: Error dehydrating activity, %s" % ae.message)
        except TypeError, te:
            self.logger.debug("TypeError: Error dehydrating activity, %s" % te.message)
        except Exception, ee:
            self.logger.debug("Exception: Error dehydrating activity, %s" % ee.message)
        return None

