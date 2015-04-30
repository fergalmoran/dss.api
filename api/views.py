import logging
import os

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http.response import HttpResponse
from django.utils.encoding import smart_str
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import detail_route
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework import filters

from api.serialisers import MixSerializer, UserProfileSerializer, NotificationSerializer, \
    ActivitySerializer, HitlistSerializer, CommentSerializer, GenreSerializer
from dss import settings
from core.tasks import create_waveform_task, archive_mix_task
from spa.models.genre import Genre
from spa.models.activity import Activity, ActivityPlay
from spa.models.mix import Mix
from spa.models.comment import Comment
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile


logger = logging.getLogger(__name__)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = (
        'comment',
        'mix__slug',
    )
    ordering_fields = (
        'id',
    )

    def perform_create(self, serializer):
        if 'mix_id' in self.request.DATA:
            try:
                mix = Mix.objects.get(pk=self.request.DATA['mix_id'])
                if mix is not None:
                    serializer.save(mix=mix, user=self.request.user.userprofile)
            except Mix.DoesNotExist:
                pass


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.annotate(mix_count=Count('mixes')).order_by('-mix_count')
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    filter_fields = (
        'slug',
    )


class MixViewSet(viewsets.ModelViewSet):
    queryset = Mix.objects.all()
    serializer_class = MixSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = (
        'waveform_generated',
        'slug',
        'user',
        'is_featured',
    )

    @detail_route()
    def stream_url(self, request, **kwargs):
        mix = self.get_object()
        return Response({'url': mix.get_stream_url()})

    def get_queryset(self):
        if 'friends' in self.request.QUERY_PARAMS:
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
        if request.FILES['file'] is None or request.DATA.get('data') is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        file_hash = request.DATA.get('data')
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
            uid = request.META.get('HTTP_UPLOAD_HASH')
            in_file = request.FILES['file'] if request.FILES else None
            file_name, extension = os.path.splitext(in_file.name)

            file_storage = FileSystemStorage(location=os.path.join(settings.CACHE_ROOT, "mixes"))
            cache_file = file_storage.save("%s%s" % (uid, extension), ContentFile(in_file.read()))
            response = 'File creation in progress'

            try:
                create_waveform_task.delay(in_file=os.path.join(file_storage.base_location, cache_file), uid=uid)
                create_waveform_task.delay(in_file=os.path.join(file_storage.base_location, cache_file), uid=uid)
            except Exception, ex:
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


class HitlistViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().annotate(mix_count=Count('mixes')).order_by('-mix_count')[0:10]
    serializer_class = HitlistSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = ActivityPlay.objects.all() #select_subclasses()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            raise PermissionDenied("Not allowed")

        return ActivityPlay.objects.filter(mix__user=user).order_by("-id")


class DownloadItemView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            mix = Mix.objects.get(uid=request.query_params['uid'])
            return Response({'url': mix.get_download_url()}, HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response("Not Found", HTTP_404_NOT_FOUND)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            raise PermissionDenied("Not allowed")

        return Notification.objects.filter(to_user=user).order_by('-date')[0:5]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        if 'q' in self.request.QUERY_PARAMS:
            rows = Genre.objects \
                .annotate(used=Count('mix')) \
                .filter(description__icontains=self.request.QUERY_PARAMS['q']) \
                .only('description') \
                .order_by('-used')
            return rows
        else:
            rows = Genre.objects \
                .annotate(used=Count('mix')) \
                .only('description') \
                .order_by('-used')
            return rows
