from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpMethodNotAllowed, HttpUnauthorized, HttpApplicationError, HttpNotImplemented
from spa.api.v1.BaseResource import BaseResource
from spa.models import Mix, UserProfile
from spa.models.activity import ActivityComment
from spa.models.comment import Comment


class CommentResource(BaseResource):
    mix = fields.ToOneField('spa.api.v1.MixResource.MixResource', 'mix')
    likes = fields.ToManyField('spa.api.v1.UserResource.UserResource',
                                    'likes', related_name='favourites',
                                    full=False, null=True)

    class Meta:
        queryset = Comment.objects.all().order_by('-date_created')
        resource_name = 'comments'
        filtering = {
            "mix": ('exact',),
        }
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def dehydrate(self, bundle):
        if bundle.obj.user is not None:
            bundle.data['avatar_image'] = bundle.obj.user.get_profile().get_avatar_image()
            bundle.data['user_url'] = bundle.obj.user.get_profile().get_absolute_url()
            bundle.data['user_name'] = bundle.obj.user.get_profile().get_nice_name()
        else:
            bundle.data['avatar_image'] = UserProfile.get_default_avatar_image()
            bundle.data['user_url'] = "/"
            bundle.data['user_name'] = "Anonymouse"

        if bundle.request.user.is_authenticated():
            bundle.data['can_edit'] = bundle.request.user.is_staff or bundle.obj.user_id == bundle.request.user.id
        else:
            bundle.data['can_edit'] = False

        return bundle

    def obj_create(self, bundle, **kwargs):
        bundle.data['user'] = bundle.request.user
        try:
            if 'mix_id' in bundle.data:
                mix = Mix.objects.get_by_id_or_slug(bundle.data['mix_id'])
                if mix is not None:
                    if bundle.request.user.is_authenticated():
                        ActivityComment(user=bundle.request.user.get_profile(), mix=mix).save()
                        return super(CommentResource, self).obj_create(bundle, user=bundle.request.user or None, mix=mix)
                    else:
                        ActivityComment(mix=mix).save()
                        return super(CommentResource, self).obj_create(bundle, mix=mix)
                else:
                    return HttpBadRequest("Unable to find mix for supplied mix_id (candidate fields are slug & id).")

            return HttpBadRequest("Missing mix_id field.")
        except ImmediateHttpResponse as e:
            self.logger.error("Error creating comment (%s)" % e)
            return HttpUnauthorized("Git tae fuck!")
        except Exception as e:
            self.logger.error("Error creating comment (%s)" % e)
            return HttpApplicationError("Unable to hydrate comment from supplied data.")
