from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Count, Q
from django.conf.urls import url

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.utils import trailing_slash
from tastypie_msgpack import Serializer
from dss import settings
from spa.api.v1.BaseResource import BaseResource
from spa.api.v1.PlaylistResource import PlaylistResource
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix


class UserResource(BaseResource):
    following = fields.ToManyField(to='self', attribute='following', related_name='following', null=True)
    followers = fields.ToManyField(to='self', attribute='followers', related_name='followers', null=True)

    favourites = fields.ToManyField('spa.api.v1.MixResource.MixResource', 'favourites', null=True)
    playlists = fields.ToManyField('spa.api.v1.PlaylistResource.PlaylistResource', 'playlists',
                                   related_name='user', null=True, full=True)

    class Meta:
        queryset = UserProfile.objects.all().annotate(mix_count=Count('mixes')).order_by('-mix_count')
        serializer = Serializer()
        resource_name = 'user'

        if not settings.DEBUG:
            excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        ordering = ['mix_count']
        filtering = {
            'slug': ALL,
            'display_name': ALL,
            'following': ALL_WITH_RELATIONS,
            'followers': ALL_WITH_RELATIONS,
            'favourites': ALL_WITH_RELATIONS,
            'playlists': ALL_WITH_RELATIONS,
        }
        authorization = Authorization()
        authentication = Authentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(UserResource, self).apply_filters(request, applicable_filters)
        q = request.GET.get('q', None)
        if q is not None:
            semi_filtered = semi_filtered.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(display_name__icontains=q)
            )

        return semi_filtered

    def obj_create(self, bundle, **kwargs):
        return super(UserResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        return super(UserResource, self).obj_update(bundle, skip_errors, **kwargs)

    def _create_playlist(self, request):
        pass

    def get_playlists(self, request, **kwargs):
        if request.method == 'POST':
            return self._create_playlist(request)
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()

        child_resource = PlaylistResource()
        return child_resource.get_list(request, mix=obj)

    def dehydrate_description(self, bundle):
        return bundle.obj.get_profile_description()

    def dehydrate(self, bundle):
        del bundle.data['activity_sharing_networks']
        bundle.data['display_name'] = bundle.obj.get_nice_name()
        bundle.data['avatar_image'] = bundle.obj.get_avatar_image()

        bundle = BaseResource.dehydrate_bitfield(
            bundle=bundle,
            field_name='email_notifications',
            object_field=bundle.obj.email_notifications,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )

        bundle = BaseResource.dehydrate_bitfield(
            bundle=bundle,
            field_name='activity_sharing_facebook',
            object_field=bundle.obj.activity_sharing_facebook,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )

        bundle = BaseResource.dehydrate_bitfield(
            bundle=bundle,
            field_name='activity_sharing_twitter',
            object_field=bundle.obj.activity_sharing_twitter,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )

        if bundle.obj.user.id == bundle.request.user.id:
            bundle.data['email'] = bundle.obj.email
            bundle.data['first_name'] = bundle.obj.first_name
            bundle.data['last_name'] = bundle.obj.last_name

        bundle.data['like_count'] = Mix.objects.filter(likes__user=bundle.obj).count()
        bundle.data['favourite_count'] = Mix.objects.filter(favourites__user=bundle.obj).count()
        # bundle.data['follower_count'] = bundle.obj.followers.count()
        bundle.data['following_count'] = bundle.obj.following.count()
        bundle.data['is_following'] = bundle.obj.is_follower(bundle.request.user)
        bundle.data['url'] = bundle.obj.get_profile_url()
        bundle.data['date_joined'] = bundle.obj.user.date_joined
        bundle.data['last_login'] = bundle.obj.user.last_login
        bundle.data['mix_count'] = bundle.obj.mix_count
        bundle.data['thumbnail'] = bundle.obj.get_small_profile_image()

        return bundle

    def hydrate(self, bundle):
        bundle = BaseResource.hydrate_bitfield(
            bundle=bundle,
            field_name='email_notifications',
            object_field=UserProfile.email_notifications,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )
        bundle = BaseResource.hydrate_bitfield(
            bundle=bundle,
            field_name='activity_sharing_facebook',
            object_field=UserProfile.activity_sharing_facebook,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )

        bundle = BaseResource.hydrate_bitfield(
            bundle=bundle,
            field_name='activity_sharing_twitter',
            object_field=UserProfile.activity_sharing_twitter,
            choices=UserProfile.NOTIFICATION_CHOICES,
        )

        return bundle

    def get_followers(self, request, **kwargs):
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        child_resource = UserResource()
        return child_resource.get_list(request, followers__in=obj)
