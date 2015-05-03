import json
# from django.core.serializers import serialize
from django.db.models import Count
from rest_framework import serializers
from dss import settings
from spa.models import Activity
from spa.models.activity import ActivityDownload, ActivityPlay
from spa.models.genre import Genre
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix, MixUpdateException
from spa.models.comment import Comment


class InlineUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'slug',
            'first_name',
            'last_name',
            'display_name',
            'avatar_image',
            'avatar_image_tiny',
        )

    first_name = serializers.ReadOnlyField(source='get_first_name')
    last_name = serializers.ReadOnlyField(source='get_last_name')
    display_name = serializers.ReadOnlyField(source='get_nice_name')
    avatar_image = serializers.SerializerMethodField()
    avatar_image_tiny = serializers.SerializerMethodField()

    def get_avatar_image(self, obj):
        return obj.get_sized_avatar_image(64, 64)

    def get_avatar_image_tiny(self, obj):
        return obj.get_sized_avatar_image(32, 32)

    def to_representation(self, instance):
        if instance.user.is_anonymous():
            return {
                'avatar_image': settings.DEFAULT_USER_IMAGE,
                'display_name': settings.DEFAULT_USER_NAME,
                'slug': ''
            }

        return super(serializers.ModelSerializer, self).to_representation(instance)


class InlineMixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mix
        fields = (
            'title',
            'slug',
            'title',
            'description',
            'mix_image',
        )

    mix_image = serializers.ReadOnlyField(source='get_image_url')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'display_name',
            'slug',
        )

    display_name = serializers.ReadOnlyField(source='get_nice_name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'slug',
            'description'
        )


class InlineActivitySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        try:
            if obj.user is not None:
                return obj.user.get_nice_name()
        except:
            pass

        return "Anomymouse"


class InlineActivityPlaySerializer(InlineActivitySerializer):
    class Meta:
        model = ActivityPlay
        fields = (
            'user',
            'date'
        )


class InlineActivityDownloadSerializer(InlineActivitySerializer):
    class Meta:
        model = ActivityDownload
        fields = (
            'user',
            'date'
        )


class MixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mix
        fields = [
            'id',
            'slug',
            'uid',
            'title',
            'description',
            'user',
            'duration',
            'waveform_url',
            'waveform_progress_url',
            'mix_image',
            # 'stream_url',
            'download_allowed',
            'can_edit',
            'genres',
            'likes',
            'favourites',
            'activity_plays',
            'activity_downloads',
            'is_liked',
        ]

    slug = serializers.ReadOnlyField(required=False)
    user = InlineUserProfileSerializer(many=False, required=False, read_only=True)
    waveform_url = serializers.ReadOnlyField(source='get_waveform_url')
    waveform_progress_url = serializers.ReadOnlyField(source='get_waveform_progress_url')
    mix_image = serializers.ReadOnlyField(source='get_image_url')
    can_edit = serializers.SerializerMethodField()

    genres = GenreSerializer(many=True, required=False, read_only=True)
    likes = LikeSerializer(many=True, required=False, read_only=False)  # slug_field='slug', many=True, read_only=True)
    favourites = serializers.SlugRelatedField(slug_field='slug', many=True, read_only=True)
    activity_plays = InlineActivityPlaySerializer(many=True, read_only=True)
    activity_downloads = InlineActivityDownloadSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    def update(self, instance, validated_data):
        # all nested representations need to be serialized separately here
        try:
            likes = validated_data['likes']

            # get any likes that aren't in passed bundle
            unliked = instance.likes.exclude(user__userprofile__slug__in=[l['slug'] for l in likes])
            for ul in unliked:
                # check that the user removing the like is an instance of the current user
                # for now, only the current user can like stuff
                if ul == self.context['request'].user.userprofile:
                    instance.update_liked(ul, False)

            for like in likes:
                # check that the user adding the like is an instance of the current user
                # for now, only the current user can like stuff
                try:
                    user = UserProfile.objects.get(slug=like['slug'])
                    if user is not None and user == self.context['request'].user.userprofile:
                        instance.update_liked(user, True)

                except UserProfile.DoesNotExist:
                    pass
            validated_data.pop('likes', None)
            return super(MixSerializer, self).update(instance, validated_data)
        except MixUpdateException, ex:
            raise ex

    def is_valid(self, raise_exception=False):
        return super(MixSerializer, self).is_valid(raise_exception)

    def get_avatar_image(self, obj):
        return obj.user.get_sized_avatar_image(32, 32)

    def get_can_edit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated():
            return user.is_staff or obj.user.id == user.userprofile.id

        return False

    def get_is_favourited(self, obj):
        user = self.context['request'].user
        return obj.is_favourited(user) if user.is_authenticated() else False

    def get_validation_exclusions(self, instance=None):
        exclusions = super(MixSerializer, self).get_validation_exclusions()
        return exclusions + ['genres', 'comments', 'slug', 'user']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.is_liked(user) if user.is_authenticated() else False


class UserProfileSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    mixes = InlineMixSerializer(many=True, required=False)
    likes = serializers.SlugRelatedField(slug_field='slug', many=True, read_only=True)
    favourites = serializers.SlugRelatedField(slug_field='slug', many=True, read_only=True)
    following = InlineUserProfileSerializer(many=True, read_only=True)
    followers = InlineUserProfileSerializer(many=True, read_only=True)
    first_name = serializers.ReadOnlyField(source='get_first_name')
    last_name = serializers.ReadOnlyField(source='get_last_name')
    display_name = serializers.ReadOnlyField(source='get_nice_name')
    isme = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    profile_image_small = serializers.SerializerMethodField()
    profile_image_medium = serializers.SerializerMethodField()
    profile_image_header = serializers.SerializerMethodField()

    top_tags = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        lookup_field = 'slug'
        fields = (
            'roles',
            'date_joined',
            'last_login',
            'first_name',
            'last_name',
            'display_name',
            'description',
            'title',
            'profile_image_small',
            'profile_image_medium',
            'profile_image_header',
            'slug',
            'mixes',
            'likes',
            'isme',
            'favourites',
            'following',
            'followers',
            'top_tags',
        )

    def get_title(self, obj):
        try:
            if obj.description:
                return obj.description[:75] + (obj.description[75:] and '..')
            else:
                return settings.DEFAULT_USER_TITLE
        except:
            return settings.DEFAULT_USER_TITLE

    def get_roles(self, obj):
        return obj.get_roles()

    def get_isme(self, obj):
        return self.context['request'].user.pk == obj.user_id

    def get_date_joined(self, obj):
        return obj.user.date_joined

    def get_last_login(self, obj):
        return obj.user.last_login

    def get_profile_image_small(self, obj):
        return obj.get_sized_avatar_image(32, 32)

    def get_profile_image_medium(self, obj):
        return obj.get_sized_avatar_image(170, 170)

    def get_profile_image_header(self, obj):
        return obj.get_sized_avatar_image(1200, 150)

    def get_top_tags(self, obj):
        return list(
            Genre.objects.filter(mix__user__slug='fergalmoran').
                annotate(total=Count('mix')).
                order_by('-total').
                values('total', 'description', 'slug')[0:3])


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    avatar_image = serializers.SerializerMethodField()
    user_display_name = serializers.SerializerMethodField('get_display_name')
    mix = serializers.PrimaryKeyRelatedField(read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment',
            'time_index',
            'date_created',
            'user',
            'user_display_name',
            'avatar_image',
            'mix',
            'can_edit',
        )

    def get_display_name(self, obj):
        if obj.user is not None:
            return obj.user.get_nice_name()
        else:
            return settings.DEFAULT_USER_NAME

    def get_avatar_image(self, obj):
        if obj.user is not None:
            return obj.user.get_sized_avatar_image(48, 48)
        else:
            return settings.DEFAULT_USER_IMAGE

    def get_can_edit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated():
            return user.is_staff or obj.user.id == user.userprofile.id

        return False


class HitlistSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField(method_name='get_display_name')
    avatar_image = serializers.SerializerMethodField(method_name='get_avatar_image')

    class Meta:
        model = UserProfile
        fields = (
            'display_name',
            'description',
            'slug',
            'avatar_image'
        )

    def get_display_name(self, obj):
        return obj.get_nice_name()

    def get_avatar_image(self, obj):
        return obj.get_sized_avatar_image(170, 170)


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    from_user = InlineUserProfileSerializer(source='get_user')
    to_user = InlineUserProfileSerializer(source='get_target_user')
    verb = serializers.CharField(source='get_verb_past')
    object_type = serializers.CharField(source='get_object_type')
    object_name = serializers.CharField(source='get_object_name')
    object_slug = serializers.CharField(source='get_object_slug')

    class Meta:
        model = Activity
        fields = (
            'id',
            'date',
            'from_user',
            'to_user',
            'verb',
            'object_type',
            'object_name',
            'object_slug',
        )


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    from_user = UserProfileSerializer(many=False, required=False)
    display_name = serializers.SerializerMethodField(method_name='get_display_name')
    avatar_image = serializers.SerializerMethodField(method_name='get_avatar_image')

    class Meta:
        model = Notification
        fields = (
            'id',
            'notification_url',
            'from_user',
            'display_name',
            'avatar_image',
            'verb',
            'target',
        )

    def get_display_name(self, obj):
        return settings.DEFAULT_USER_NAME if obj.from_user is None else obj.from_user.get_nice_name()

    def get_avatar_image(self, obj):
        return settings.DEFAULT_USER_IMAGE if obj.from_user is None else obj.from_user.get_sized_avatar_image(170, 170)
