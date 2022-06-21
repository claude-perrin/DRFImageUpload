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
from easy_thumbnails.alias import aliases

# from .management import MyUserManager
from rest_framework.authtoken.admin import User


# TODO You don't have expiring links to binary images
# TODO docker-compose
# TODO thumnails should be a list somehow

class Thumbnail(models.Model):
    size = models.CharField(max_length=10, default='0x0')

    def __str__(self):
        return f"{self.size}"


class Tier(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='')
    thumbnails = models.ManyToManyField(
        Thumbnail,
        blank=False,
        null=True,
    )
    link = models.BooleanField(default=True)
    expiring_links = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # you can check if object just created by comparing "pk" attr to None
        # you can also use _state attr see doc link below
        is_created = self.pk is None

        super(Tier, self).save(*args, **kwargs)

        if is_created:
            # do something here
            if not aliases.get(self.name):
                for thumbnail in self.thumbnails.all():
                    thumbnail_height, thumbnail_width = self.thumbnail.split('x')
                    aliases.set(self.name, {'size': (thumbnail_height, thumbnail_width), 'crop': True})
                    print(aliases.get('Basic'))

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
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user}"


def upload_to(instance, filename):
    return f'images/{filename}'


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
