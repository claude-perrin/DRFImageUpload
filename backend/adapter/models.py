from datetime import datetime

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL  # auth.User


class AttachmentDownloadStatus(models.TextChoices):
    PENDING = 'pending', 'pending'
    FAILED = 'failed', 'failed'
    VANISHED = 'vanished', 'vanished'
    FINISHED = 'finished', 'finished'


def upload_to(instance, filename):
    return f'images/{filename}'



class Image(models.Model):
    description = models.CharField(max_length=40, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to=upload_to)
