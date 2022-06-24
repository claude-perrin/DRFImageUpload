import base64
import datetime
import os
import subprocess

from django.conf import settings
from rest_framework import serializers

from .models import Image, Profile, Tier, Thumbnail, Token
from PIL import Image as PIL_IMAGE


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
            'original_image_link',
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


# TODO it is better to separate input and output images

class ImageSubmitSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Image
        fields = [
            'description',
            'profile',
            'image',
        ]


class ImageSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    profile = ProfileSerializer(write_only=True)
    thumbnail = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.profile.tier.original_image_link:
            request = self.context.get('request')
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)

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
                request = self.context.get('request')
                thumbnail_links.append(request.build_absolute_uri(f'/media/{folder_path}/{thumbnail_name}'))
        return thumbnail_links


def generate_token(expiration_time):
    expire_at = datetime.datetime.now() + datetime.timedelta(seconds=expiration_time)
    token = Token.objects.create(expiration=expire_at)
    return token.token


class ImageCreateBinarySerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)
    binary_image = serializers.SerializerMethodField()

    def get_binary_image(self, obj):
        if obj.profile.tier.expiring_links:
            request = self.context.get('request')
            token = generate_token(self.context.get('expiration_time'))

            image_path = obj.image.path
            _, image_name = str(obj.image).split('/')
            output_path = 'media/binary/BINARY-'
            with PIL_IMAGE.open(image_path).convert('1') as image:
                image.save(f'{output_path}{image_name}')
            return request.build_absolute_uri(f'{token}/BINARY-{image_name}')
