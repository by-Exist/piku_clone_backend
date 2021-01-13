# https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c

from pprint import pprint
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


def get_upload_path(instance, filename):
    name = instance.album.model.__class__._meta.verbose_name_plural.replace(" ", "_")
    return f"{name}/images/%Y/%m/%d/%h/{filename}"


# TODO: 썸네일, 타이틀 추가
class Album(models.Model):

    MEDIA_TYPES = [
        ("T", "text"),
        ("I", "image"),
        ("G", "gif"),  # convert to mp4
        ("V", "video"),
    ]

    media_type = models.CharField(
        "데이터 타입", max_length=1, choices=MEDIA_TYPES, default=None
    )

    # FIXME: AlbumSerializer의 어떤 동작 과정때문인지는 몰라도 쿼리가 4번씩 반복된다. 추후 수정.
    @property
    def media_list(self):
        for M, media_type in self.MEDIA_TYPES:
            if self.media_type == M:
                attr = f"{media_type}_set"
                return getattr(self, attr).values_list("media", flat=True)
        return []  # FIXME: return이 좀 더 적절하게 구성되는 방법이 없을까?


class Text(models.Model):
    album = models.ForeignKey(Album, related_name="text_set", on_delete=models.CASCADE)
    media = models.CharField("텍스트", max_length=511)


class Image(models.Model):
    album = models.ForeignKey(Album, related_name="image_set", on_delete=models.CASCADE)
    media = models.FileField("이미지 파일", upload_to=get_upload_path)


class Gif(models.Model):
    album = models.ForeignKey(Album, related_name="gif_set", on_delete=models.CASCADE)
    media = models.FileField("움짤 파일 (gif -> mp4)", upload_to=get_upload_path)


class Video(models.Model):
    album = models.ForeignKey(Album, related_name="video_set", on_delete=models.CASCADE)
    media = models.CharField("외부 비디오 링크", max_length=511)


class WorldcupManager(models.Manager):
    def create_with_album(self, worldcup_data=None, album_data=None):

        worldcup = Worldcup(**worldcup_data)
        album = Album(**album_data)
        album.save()
        worldcup.album = album
        worldcup.save()

        return worldcup

    def update_with_album(self, worldcup, worldcup_data=None, album_data=None):

        worldcup = worldcup
        album = worldcup.album

        if worldcup_data:
            for key, value in worldcup_data.items():
                setattr(worldcup, key, value)
            worldcup.save()

        if album_data:
            for key, value in album_data.items():
                setattr(album, key, value)
            album.save()

        return worldcup


# TODO: 썸네일, 공개방식, 암호, 좋아요 구현
class Worldcup(models.Model):

    objects = WorldcupManager()

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자", editable=False
    )
    album = models.OneToOneField(
        Album,
        related_name="model",
        on_delete=models.CASCADE,
        verbose_name="앨범",
    )

    title = models.CharField("제목", max_length=127)
    intro = models.CharField("소개", max_length=255)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    play_count = models.PositiveIntegerField("플레이 횟수", default=0, editable=False)

    def __str__(self):
        return self.title