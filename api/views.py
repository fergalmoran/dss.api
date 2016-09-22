import logging
import os
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Q
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import detail_route
from rest_framework.permissions import BasePermission
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from api import serializers
from dss import settings
from spa import tasks
from spa.models import Message, Playlist
from spa.models.blog import Blog
from spa.models.genre import Genre
from spa.models.activity import ActivityPlay
from spa.models.mix import Mix
from spa.models.comment import Comment
from spa.models.notification import Notification
from spa.models.show import Show
from spa.models.userprofile import UserProfile

logger = logging.getLogger('dss')


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
            except Exception as ex:
                pass


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.annotate(mix_count=Count('mixes')).order_by('-mix_count')
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    filter_fields = (
        'slug',
        'user__first_name',
    )

    def get_queryset(self):
        if 'following' in self.request.query_params:
            ret = UserProfile.objects.filter(following__slug__in=[self.request.query_params['following']])
        elif 'followers' in self.request.query_params:
            ret = UserProfile.objects.filter(followers__slug__in=[self.request.query_params['followers']])
        elif 'messaged_with' in self.request.query_params:
            ret = UserProfile.objects.filter(messages__slug__in=[self.request.query_params['followers']])
        elif 'initial' in self.request.query_params:
            ret = UserProfile.objects.filter(user__first_name__startswith=self.request.query_params['initial']) \
                                     .annotate(mix_count=Count('mixes')).order_by('-mix_count')
        else:
            ret = super(UserProfileViewSet, self).get_queryset()

        return ret


class MixViewSet(viewsets.ModelViewSet):
    queryset = Mix.objects.all().extra({
        'play_count': 'SELECT COUNT(*) FROM spa_activityplay WHERE mix_id = spa_mix.id'
    })

    serializer_class = serializers.MixSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    filter_fields = (
        'waveform_generated',
        'slug',
        'user__slug',
        'is_featured',
        'genres__slug',
    )

    ordering_fields = (
        'id',
        'play_count'
    )

    @detail_route()
    def stream_url(self, request, **kwargs):
        mix = self.get_object()
        return Response({'url': mix.get_stream_url()})

    def get_queryset(self):
        if 'friends' in self.request.query_params:
            if self.request.user.is_authenticated():
                return self.queryset.filter(user__in=self.request.user.userprofile.following.all())
            else:
                raise PermissionDenied("Not allowed")
        if 'random' in self.request.query_params:
            return self.queryset.order_by('?').all()
        if 'slug' in self.kwargs or 'user__slug' in self.kwargs:
            """ could be private mix so don't filter """
            return self.queryset
        else:
            return self.queryset.filter(is_private=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)


class AttachedImageUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        if request.data['file'] is None or request.data.get('data') is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']
        file_hash = request.data.get('data')
        try:
            mix = Mix.objects.get(uid=file_hash)
            if mix:
                mix.mix_image = file_obj
                mix.save()
                return Response(HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.exception(ex)

        return Response(status=HTTP_401_UNAUTHORIZED)


class SearchResultsView(views.APIView):
    def get(self, request, format=None):
        q = request.GET.get('q', '')
        q_type = request.GET.get('type', '')
        if len(q) > 0:
            if q_type == 'user':
                r_s = [
                    {
                        'id': user.id,
                        'display_name': user.get_nice_name(),
                        'image': user.get_sized_avatar_image(64, 64),
                        'slug': user.slug,
                        'url': user.get_absolute_url(),
                        'description': user.description
                    } for user in UserProfile.objects.filter(
                            Q(user__first_name__icontains=q) |
                            Q(user__last_name__icontains=q) |
                            Q(display_name__icontains=q)).exclude(slug__isnull=True).exclude(slug__exact='')[0:10]
                    ]
            else:
                r_s = [
                    {
                        'id': mix.id,
                        'title': mix.title,
                        'image': mix.get_image_url(size='48x48'),
                        'user': mix.user.slug,
                        'slug': mix.slug,
                        'user': mix.user.slug,
                        'url': mix.get_absolute_url(),
                        'description': mix.description
                    } for mix in Mix.objects.filter(title__icontains=q)[0:10]]
            return Response(r_s)

        return HttpResponse(status=HTTP_204_NO_CONTENT)


class PartialMixUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    # TODO have to make this anonymous (for now) because dropzone doesn't play nice with JWT
    # permission_classes = (IsAuthenticated,)

    # noinspection PyBroadException
    def post(self, request):
        try:
            logger.info("Received post file")
            uid = request.META.get('HTTP_UPLOAD_HASH')
            session_id = request.META.get('HTTP_SESSION_ID')
            logger.info("Session Id: {0}".format(session_id))

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

                # Chain the waveform & archive tasks together
                # Probably not the best place for them but will do for now
                # First argument to upload_to_cdn_task is not specified as it is piped from create_waveform_task

                logger.debug("Processing input_file: {0}".format(input_file))
                logger.debug("Connecting to broker: {0}".format(settings.BROKER_URL))

                from celery import group, chain
                (
                    tasks.create_waveform_task.s(input_file, uid) |
                    tasks.upload_to_cdn_task.subtask(('mp3', uid, 'mixes'), immutable=True) |
                    tasks.upload_to_cdn_task.subtask(('png', uid, 'waveforms'), immutable=True) |
                    tasks.notify_subscriber.subtask((session_id, uid), immutable=True)
                ).delay()
                logger.debug("Waveform task started")

            except Exception as ex:
                logger.exception(ex)
                response = \
                    'Unable to connect to rabbitmq, there may be a delay in getting your mix online'

            file_dict = {
                'response': response,
                'size': in_file.size,
                'uid': uid
            }
            return Response(file_dict, HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.exception(ex)
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

        ret = ActivityPlay.objects.filter(mix__user=user.userprofile).order_by("-id")

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

        return Notification.objects.filter(to_user=user.userprofile).order_by('-id')

    def perform_update(self, serializer):
        return super(NotificationViewSet, self).perform_update(serializer)


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


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if 'to_user' in self.request.query_params and 'type' in self.request.query_params:
            t = UserProfile.objects.get(slug=self.request.query_params['to_user'])
            try:
                if self.request.query_params['type'] == 'chat':
                    return Message.objects.get_chat(user1=t, user2=self.request.user.userprofile)
            except UserProfile.DoesNotExist:
                pass

        raise SuspiciousOperation("Must specify a to user")

    def __perform_write(self, serializer):
        t = None
        if 'to_user' in self.request.data:
            t = UserProfile.objects.get(slug=self.request.data['to_user'])

        serializer.save(from_user=self.request.user.userprofile, to_user=t)

    def perform_create(self, serializer):
        self.__perform_write(serializer)

    def perform_update(self, serializer):
        self.__perform_write(serializer)


class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = serializers.ShowSerializer

    def perform_create(self, serializer):
        try:
            performer = UserProfile.objects.get(pk=self.request.data['performer'])
            serializer.save(user=self.request.user.userprofile, performer=performer)
        except UserProfile.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST, data='Performer not found')
        except Exception as ex:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR, data=ex)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user.userprofile)

        return Response(status=HTTP_401_UNAUTHORIZED)
