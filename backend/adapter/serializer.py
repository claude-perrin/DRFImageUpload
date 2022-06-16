from easy_thumbnails_rest.serializers import ThumbnailerSerializer
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from .models import Image, MyUser, Tier

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

HOST_URL = "http://127.0.0.1:8000"


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = [
            'name',
            'thumbnails',
            'link',
            'expiring_links',
        ]


class UserSerializer(serializers.ModelSerializer):
    tier = TierSerializer()

    class Meta:
        model = MyUser
        fields = [
            'username',
            'tier',
        ]


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    avatar = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Image
        fields = [
            'user',
            'description',
            'image',
            'avatar',
        ]

    def get_avatar(self, obj):
        return HOST_URL + thumbnail_url(obj.image, 'avatar')

    # return get_thumbnail(obj, '200x200', crop='center', quality=99).url
