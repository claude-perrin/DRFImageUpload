import binascii
import os
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver

# from .management import MyUserManager
from rest_framework.authtoken.admin import User


# TODO a link ..../view/binary/400(time) -> returns all binary images generated for 400sec
# TODO in the view, time is taken -> Token is generated -> token is put into the link
# TODO in retrieve, token is taken -> Time is verified
# TODO docker-compose
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class Thumbnail(models.Model):
    dimension = models.CharField(max_length=10, default='0x0')

    def __str__(self):
        return f"{self.dimension}"


class Tier(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='')
    thumbnails = models.ManyToManyField(
        Thumbnail,
        blank=False,

    )
    original_image_link = models.BooleanField(default=True)
    expiring_links = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    tier = models.ForeignKey(
        Tier,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user}"


def upload_to(instance, filename):
    return f'images/{filename}'


class Token(models.Model):
    token = models.CharField(max_length=20, default=generate_key)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"{self.token}"


class Image(models.Model):
    # Tier foreign key
    description = models.CharField(max_length=40, default='')
    image = models.ImageField(upload_to=upload_to)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.description}"


@receiver(post_save, sender=User)
def imported_info_update(sender, instance=None, created=False, **kwargs):
    if created:
        obj = Profile.objects.get_or_create(user=instance)
