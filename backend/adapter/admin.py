from django.contrib import admin

# Register your models here.
from .models import Image, Tier, UserProfile

admin.site.register(Image)
admin.site.register(Tier)
admin.site.register(UserProfile)
