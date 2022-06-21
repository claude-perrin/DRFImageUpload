import subprocess

from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import Image, Profile, Tier, Thumbnail

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

HOST_URL = "http://localhost:8000"


class ThumbnailSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(required=True)

    class Meta:
        model = Thumbnail
        fields = [
            'dimension',
        ]


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


# TODO maybe it is better to separate input and output images


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

    @staticmethod
    def create_thumbnail(input_path, thumbnail_path, thumbnail_dimension):
        command = [
            'vipsthumbnail',
            f'--size={thumbnail_dimension}>',
            input_path,
            '-o',
            f'{thumbnail_path}',
        ]

        result = subprocess.run(command, capture_output=True)
        return result.returncode

    def get_thumbnail(self, obj):
        thumbnail_links = list()
        input_path = f'{settings.MEDIA_ROOT}/{obj.image}'
        folder_path, image_name = str(obj.image).split('/')

        for thumbnail in obj.profile.tier.thumbnails.all():
            thumbnail_name = f'{thumbnail.dimension}-{image_name}'
            return_code = self.create_thumbnail(input_path=input_path, thumbnail_path=thumbnail_name,
                                                thumbnail_dimension=thumbnail.dimension)
            if return_code == 0:
                thumbnail_links.append(f'{HOST_URL}/media/{folder_path}/{thumbnail_name}')
        return thumbnail_links

    # return HOST_URL + thumbnail_url(obj.image, f'{obj.profile.tier.name}')
