import logging
import os

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import detail_route
from rest_framework.permissions import BasePermission
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_200_OK, HTTP_204_NO_CONTENT

from api import serializers
from core.utils.cdn import upload_to_azure
from dss import settings
from core.tasks import create_waveform_task, archive_mix_task
from spa.models.genre import Genre
from spa.models.activity import ActivityPlay
from spa.models.mix import Mix
from spa.models.comment import Comment
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile

logger = logging.getLogger('spa')


class AnonymousWriteUserDelete(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AnonymousWriteUserDelete,)
    filter_fields = (
        'comment',
        'mix__slug',
    )
    ordering_fields = (
        'id',
    )

    def perform_create(self, serializer):
        if 'mix_id' in self.request.data:
            try:
                mix = Mix.objects.get(pk=self.request.data['mix_id'])
                if mix is not None:
                    serializer.save(
                        mix=mix,
                        user=self.request.user if self.request.user.is_authenticated() else None
                    )
            except Mix.DoesNotExist:
                pass
            except Exception, ex:
                pass


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.annotate(mix_count=Count('mixes')).order_by('-mix_count')
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    filter_fields = (
        'slug',
    )

    def get_queryset(self):
        if 'following' in self.request.query_params:
            ret = UserProfile.objects.filter(following__slug__in=[self.request.query_params['following']])
        elif 'followers' in self.request.query_params:
            ret = UserProfile.objects.filter(followers__slug__in=[self.request.query_params['followers']])
        else:
            ret = super(UserProfileViewSet, self).get_queryset()

        return ret


class MixViewSet(viewsets.ModelViewSet):
    queryset = Mix.objects.all()
    serializer_class = serializers.MixSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    filter_fields = (
        'waveform_generated',
        'slug',
        'user__slug',
        'is_featured',
    )

    @detail_route()
    def stream_url(self, request, **kwargs):
        mix = self.get_object()
        return Response({'url': mix.get_stream_url()})

    def get_queryset(self):
        if 'friends' in self.request.query_params:
            if self.request.user.is_authenticated():
                rows = Mix.objects.filter(user__in=self.request.user.userprofile.following.all())
                return rows
            else:
                raise PermissionDenied("Not allowed")
        else:
            return Mix.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)


class AttachedImageUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        if request.FILES['file'] is None or request.data.get('data') is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        file_hash = request.data.get('data')
        try:
            mix = Mix.objects.get(uid=file_hash)
            if mix:
                mix.mix_image = file_obj
                mix.save()
                return Response(HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_401_UNAUTHORIZED)


class SearchResultsView(views.APIView):
    def get(self, request, format=None):
        q = request.GET.get('q', '')
        if len(q) > 0:
            m = [{
                     'title': mix.title,
                     'image': mix.get_image_url(),
                     'slug': mix.slug,
                     'url': mix.get_absolute_url(),
                     'description': mix.description
                 } for mix in Mix.objects.filter(title__icontains=q)[0:10]]
            return Response(m)

        return HttpResponse(status=HTTP_204_NO_CONTENT)


class PartialMixUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    # noinspection PyBroadException
    def post(self, request):
        try:
            logger.info("Received post file")
            uid = request.META.get('HTTP_UPLOAD_HASH')
            in_file = request.data['file'] if request.data else None
            file_name, extension = os.path.splitext(in_file.name)

            logger.info("Constructing storage")
            file_storage = FileSystemStorage(location=os.path.join(settings.CACHE_ROOT, "mixes"))
            cache_file = file_storage.save("%s%s" % (uid, extension), ContentFile(in_file.read()))
            response = 'File creation in progress'

            logger.info("Storage constructed")

            try:
                logger.debug("Received input file")
                logger.debug("Storage is {0}".format(file_storage.base_location))
                input_file = os.path.join(file_storage.base_location, cache_file)
                logger.debug("Input file generating")

                # Chain the waveform & archive tasks together
                # Probably not the best place for them but will do for now
                # First argument to archive_mix_task is not specified as it is piped from create_waveform_task
                (create_waveform_task.s(input_file, uid) |
                 archive_mix_task.s(filetype='mp3', uid=uid)).delay()

            except Exception, ex:
                logger.error("Unable to connect to celery: {0}".format(ex.message))
                response = \
                    'Unable to connect to waveform generation task, there may be a delay in getting your mix online'

            file_dict = {
                'response': response,
                'size': in_file.size,
                'uid': uid
            }
            return Response(file_dict, HTTP_202_ACCEPTED)
        except Exception, ex:
            logger.exception(ex.message)
            raise


class HitlistViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().annotate(mix_count=Count('mixes')).order_by('-mix_count')[0:10]
    serializer_class = serializers.HitlistSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = ActivityPlay.objects.all()  # select_subclasses()
    serializer_class = serializers.ActivitySerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            raise PermissionDenied("Not allowed")

        ret = ActivityPlay.objects.filter(mix__user=user).order_by("-id")

        if len(ret) > 0:
            logger.debug("Activity returned: {0}".format(ret[0].get_object_slug()))
            return ret
        else:
            return []


class DownloadItemView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            mix = Mix.objects.get(uid=request.query_params['uid'])
            return Response({'url': mix.get_download_url()}, HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response("Not Found", HTTP_404_NOT_FOUND)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            raise PermissionDenied("Not allowed")

        return Notification.objects.filter(to_user=user).order_by('-date')[0:5]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer

    def get_queryset(self):
        if 'q' in self.request.query_params:
            rows = Genre.objects \
                .annotate(used=Count('mix')) \
                .filter(description__icontains=self.request.query_params['q']) \
                .only('description') \
                .order_by('-used')
            return rows
        else:
            rows = Genre.objects \
                .annotate(used=Count('mix')) \
                .only('description') \
                .order_by('-used')
            return rows
