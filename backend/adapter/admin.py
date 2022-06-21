from django.contrib import admin

# Register your models here.
from .models import Image, Tier, Profile, Thumbnail


class TierInline(admin.TabularInline):
    model = Tier.thumbnails.through


class ThumbnailAdmin(admin.ModelAdmin):
    inlines = [TierInline, ]


class ThumbnailSizesAdmin(admin.ModelAdmin):
    inlines = [
        ThumbnailAdmin,
    ]
    exclude = ('thumbnails',)


admin.site.register(Image)
admin.site.register(Tier)
admin.site.register(Profile)
admin.site.register(Thumbnail, ThumbnailAdmin)
