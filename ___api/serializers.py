from rest_framework import serializers
from spa import models


class MixSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = models.Mix


class UserProfileSerializer(serializers.ModelSerializer):
    mixes = serializers.HyperlinkedRelatedField(queryset=models.Mix.objects.all(), view_name='mix-detail', many=True)

    class Meta:
        model = models.UserProfile
