from django.contrib import admin
from pikuapp.models import (
    Text,
    Image,
    Album,
    TextComment,
    ImageComment,
    Comment,
    Worldcup,
)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(TextComment)
class TextCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageComment)
class ImageCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Worldcup)
class WorldcupAdmin(admin.ModelAdmin):
    pass
