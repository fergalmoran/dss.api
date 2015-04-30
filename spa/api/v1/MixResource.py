from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count
from django.http import Http404
from django.template.loader import render_to_string
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.fields import ToOneField
from tastypie.http import HttpGone, HttpUnauthorized
from tastypie.utils import trailing_slash
from dss import settings

from spa.api.v1.BaseResource import BaseResource
from spa.api.v1.CommentResource import CommentResource
from spa.api.v1.ActivityResource import ActivityResource
from spa.models.mix import Mix
from spa.models.show import Show
from spa.models.userprofile import UserProfile


class MixResource(BaseResource):
    comments = fields.ToManyField('spa.api.v1.CommentResource.CommentResource',
                                  'comments', null=True, full=True)
    favourites = fields.ToManyField('spa.api.v1.UserResource.UserResource',
                                    'favourites', related_name='favourites',
                                    full=False, null=True)
    likes = fields.ToManyField('spa.api.v1.UserResource.UserResource',
                               'likes', related_name='likes',
                               full=False, null=True)
    genres = fields.ToManyField('spa.api.v1.GenreResource.GenreResource',
                                'genres', related_name='genres',
                                full=True, null=True)

    class Meta:
        queryset = Mix.objects.filter(is_active=True)
        user = ToOneField('UserResource', 'user')
        always_return_data = True
        detail_uri_name = 'slug'
        excludes = ['is_active', 'waveform-generated']
        post_excludes = ['comments']
        filtering = {'comments': ALL_WITH_RELATIONS,
                     'genres': ALL_WITH_RELATIONS,
                     'favourites': ALL_WITH_RELATIONS,
                     'likes': ALL_WITH_RELATIONS,
                     'title': ALL_WITH_RELATIONS,
                     'slug': ALL_WITH_RELATIONS, }
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"),
            url(r"^(?P<resource_name>%s)/(?P<id>[\d]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/random%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_random'), name="api_dispatch_random"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d-]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/comments%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/activity%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_activity'), name="api_get_activity"),
        ]

    def dispatch_random(self, request, **kwargs):
        kwargs['pk'] = \
            self._meta.queryset.values_list('pk', flat=True).order_by('?')[0]
        return self.get_detail(request, **kwargs)

    def get_comments(self, request, **kwargs):
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()

        child_resource = CommentResource()
        return child_resource.get_list(request, mix=obj)

    def get_activity(self, request, **kwargs):
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()

        child_resource = ActivityResource()
        return child_resource.get_list(request, mix=obj)

    def obj_create(self, bundle, **kwargs):
        if 'is_featured' not in bundle.data:
            bundle.data['is_featured'] = False

        if 'download_allowed' not in bundle.data:
            bundle.data['download_allowed'] = False

        #AAAAAH - STOP BEING LAZY AND REMOVE THIS

        if settings.DEBUG and bundle.request.user.is_anonymous():
            bundle.data['user'] = UserProfile.objects.get(pk=2)
        else:
            bundle.data['user'] = bundle.request.user.get_profile()

        ret = super(MixResource, self).obj_create(
            bundle,
            user=bundle.data['user'],
            uid=bundle.data['upload-hash'],
            extension=bundle.data['upload-extension'])

        return ret

    def obj_update(self, bundle, **kwargs):
        #don't sync the mix_image, this has to be handled separately
        bundle.data.pop('mix_image', None)

        ret = super(MixResource, self).obj_update(bundle, bundle.request)

        bundle.obj.update_favourite(bundle.request.user,
                                    bundle.data['favourited'])
        bundle.obj.update_liked(bundle.request.user,
                                bundle.data['liked'])

        return ret

    def apply_sorting(self, obj_list, options=None):
        orderby = options.get('order_by', '')
        if orderby == 'latest':
            obj_list = obj_list.order_by('-id')
        elif orderby == 'toprated':
            obj_list = obj_list.annotate(
                karma=Count('activity_likes')).order_by('-karma')
        elif orderby == 'mostplayed':
            obj_list = obj_list.annotate(
                karma=Count('activity_plays')).order_by('-karma')
        elif orderby == 'mostactive':
            obj_list = obj_list.annotate(
                karma=Count('comments')).order_by('-karma')
        elif orderby == 'recommended':
            obj_list = obj_list.annotate(
                karma=Count('activity_likes')).order_by('-karma')

        return obj_list

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(MixResource, self) \
            .apply_filters(request, applicable_filters) \
            .filter(waveform_generated=True)

        f_user = request.GET.get('user', None)

        if request.GET.get('stream'):
            if request.user.is_anonymous():
                raise ImmediateHttpResponse(
                    HttpUnauthorized("Only logged in users have a stream")
                )
            semi_filtered = semi_filtered.filter(
                user__in=request.user.get_profile().following.all())

        if request.GET.get('for_show'):
            semi_filtered = semi_filtered.filter(show__isnull=True)

        if f_user is not None:
            semi_filtered = semi_filtered.filter(user__slug=f_user)
        elif len(applicable_filters) == 0:
            semi_filtered = semi_filtered.filter(is_featured=True)

        return semi_filtered

    def dehydrate_mix_image(self, bundle):
        return bundle.obj.get_image_url(size="160x110")

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        bundle.data['audio_src'] = bundle.obj.get_stream_url()
        bundle.data['user_name'] = bundle.obj.user.get_nice_name()
        bundle.data['user_profile_url'] = bundle.obj.user.get_absolute_url()
        bundle.data['user_profile_image'] = \
            bundle.obj.user.get_small_profile_image()
        bundle.data['item_url'] = '/mix/%s' % bundle.obj.slug
        bundle.data['download_allowed'] = bundle.obj.download_allowed
        bundle.data['favourite_count'] = bundle.obj.favourites.count()

        bundle.data['play_count'] = bundle.obj.activity_plays.count()
        bundle.data['download_count'] = bundle.obj.activity_downloads.count()
        bundle.data['like_count'] = bundle.obj.activity_likes.count()

        bundle.data['tooltip'] = render_to_string('inc/player_tooltip.html',
                                                  {'item': bundle.obj})
        bundle.data['comment_count'] = bundle.obj.comments.count()

        bundle.data['liked'] = bundle.obj.is_liked(bundle.request.user)

        if bundle.request.user.is_authenticated():
            bundle.data['can_edit'] = bundle.request.user.is_staff or \
                bundle.obj.user_id == bundle.request.user.get_profile().id
        else:
            bundle.data['can_edit'] = False

        if bundle.request.user.is_authenticated():
            bundle.data['favourited'] = bundle.obj.favourites.filter(
                user=bundle.request.user).count() != 0
        else:
            bundle.data['favourited'] = False

        return bundle

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = Mix.objects.filter(title__icontains=request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {'objects': objects, }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
