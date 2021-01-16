from django.contrib import admin
from . import models


@admin.register(models.Worldcup)
class WorldcupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Gif)
class GifAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    pass
