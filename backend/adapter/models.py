import binascii
import os
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver

from rest_framework.authtoken.admin import User

from .models_helper import *


class Thumbnail(models.Model):
    dimension = models.CharField(max_length=10, default='0x0', validators=[validate_thumbnail_format], unique=True)

    def __str__(self):
        return f"{self.dimension}"


class Tier(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='')
    thumbnails = models.ManyToManyField(Thumbnail, blank=False)
    original_image_link = models.BooleanField(default=True)
    expiring_links = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, )
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, blank=True, null=True, )

    def __str__(self):
        return f"{self.user}"


class Token(models.Model):
    token = models.CharField(max_length=20, default=generate_key)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"{self.token}"


class Image(models.Model):
    # Tier foreign key
    description = models.CharField(max_length=40, default='')
    image = models.ImageField(upload_to=upload_to)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return f"{self.description}"


"""
Creates an empty profile for a just created user
"""


@receiver(post_save, sender=User)
def imported_info_update(sender, instance=None, created=False, **kwargs):
    if created:
        obj = Profile.objects.get_or_create(user=instance)
