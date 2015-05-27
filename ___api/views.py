from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ___api import serializers
from spa import models


class MixViewSet(viewsets.ModelViewSet):
    queryset = models.Mix.objects.all()
    serializer_class = serializers.MixSerializer

    filter_fields = (
        'waveform_generated',
        'slug',
        'user',
        'is_featured',
    )

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all().order_by('-id')  # annotate(mix_count=Count('mixes')).order_by('-mix_count')
    serializer_class = serializers.UserProfileSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    filter_fields = (
        'slug',
    )
