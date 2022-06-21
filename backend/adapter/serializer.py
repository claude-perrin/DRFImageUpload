from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import Image, Profile, Tier

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

HOST_URL = "http://localhost:8000"


class TierSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Tier
        fields = [
            'name',
            'thumbnails',
            'link',
            'expiring_links',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    tier = TierSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'tier',
        ]


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    profile = ProfileSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'description',
            'profile',
            'image',
            'thumbnail',
        ]

    def get_thumbnail(self, obj):
        # return self.context.get('alias')
        return HOST_URL + thumbnail_url(obj.image, f'{obj.profile.tier.name}')
