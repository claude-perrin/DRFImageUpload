from datetime import datetime

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import models as auth_models

from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.fields import ThumbnailerField
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from .management import MyUserManager


def upload_to(instance, filename):
    return f'images/{filename}'


class Tier(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='')
    thumbnails = models.CharField(max_length=10, default='0x0')
    link = models.BooleanField(default=True)
    expiring_links = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    # Tier foreign key
    description = models.CharField(max_length=40, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to=upload_to)


class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, default='username')
    tier = models.ForeignKey(Tier, blank=True, null=True, related_name='Tier', on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.username
