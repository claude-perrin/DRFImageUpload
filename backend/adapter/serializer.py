import base64
import datetime
import os
import subprocess

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Image, Profile, Tier, Thumbnail, Token
from PIL import Image as PIL_Image


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
        depth = 1


class ImageSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    profile = ProfileSerializer(write_only=True)
    thumbnail = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.profile.tier.original_image_link:
            request = self.context.get('request')
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)

    """
    Uses vipsthumbnail console command to make a thumbnail
    If created successfully returns True otherwise False
    """

    @staticmethod
    def create_thumbnail(input_path, thumbnail_path, thumbnail_dimension):
        command = [
            'vipsthumbnail',
            f'--size={thumbnail_dimension}>',
            input_path,
            '-o',
            thumbnail_path,
        ]

        result = subprocess.run(command, capture_output=True)
        thumbnail_created = True if result.returncode == 0 else False
        return thumbnail_created

    """
    For all images creates a thumbnail and saves it in media/images folder
    """

    def get_thumbnail(self, obj):
        thumbnail_links = list()
        input_path = f'{settings.MEDIA_ROOT}/{obj.image}'
        print(input_path)
        folder_path, image_name = str(obj.image).split('/')

        for thumbnail in obj.profile.tier.thumbnails.all():
            thumbnail_name = f'{thumbnail.dimension}-{image_name}'
            thumbnail_created = self.create_thumbnail(input_path=input_path, thumbnail_path=thumbnail_name,
                                                      thumbnail_dimension=thumbnail.dimension)
            if thumbnail_created:
                request = self.context.get('request')
                thumbnail_links.append(request.build_absolute_uri(f'/media/{folder_path}/{thumbnail_name}'))
        return thumbnail_links


def generate_token(expiration_time):
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
    token = Token.objects.create(expiration=expire_at)
    return token.token


def validate_expiration_time(value):
    if 300 < value < 300000:
        return value
    raise ValidationError("The expiration time must be in range 300-300000")


"""
1) creates an expiring token for each binary image
2) returns a link to a binary image 
"""


class ImageCreateBinarySerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)
    binary_image = serializers.SerializerMethodField()

    def get_binary_image(self, obj):
        if obj.profile.tier.expiring_links:
            request = self.context.get('request')
            expiration_time = validate_expiration_time(self.context.get('expiration_time'))

            token = generate_token(expiration_time)
            image_path = obj.image.path
            _, image_name = str(obj.image).split('/')
            output_path = settings.MEDIA_ROOT + '/binary/BINARY-' + image_name

            with PIL_Image.open(image_path).convert('1') as image:
                image.save(output_path)
            return request.build_absolute_uri(f'{token}/BINARY-{image_name}')
