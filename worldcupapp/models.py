# https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c

from backend.settings.dev import MEDIA_ROOT
from pprint import pprint
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator


User = get_user_model()


class Album(models.Model):

    MEDIA_TYPES = [
        ("T", "text"),
        ("I", "image"),
        ("G", "gif"),  # convert to mp4
        ("V", "video"),
    ]

    # TODO: 썸네일 추가 (썸네일을 만들어 저장하는 과정을 셀러리로 구현해보자)
    # thumbnail = models.ImageField("썸네일", upload_to="Album/thumbnail/%Y/%m/%d/")
    media_type = models.CharField(
        "데이터 타입", max_length=1, choices=MEDIA_TYPES, default=None
    )
    thumbnail = models.ImageField(
        "썸네일", editable=False, upload_to="worldcupapp/album/thumbnail/%Y/%m/%d/"
    )

    def get_media_model(self):
        MEDIA_TYPES = {
            "T": Text,
            "I": Image,
            "G": Gif,
            "V": Video,
        }
        return MEDIA_TYPES[self.media_type]


class Text(models.Model):
    album = models.ForeignKey(Album, related_name="text_set", on_delete=models.CASCADE)
    media = models.CharField("텍스트", max_length=511)
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)

    def __str__(self):
        return f"text, {self.win_count}, {self.choice_count}"


class Image(models.Model):
    album = models.ForeignKey(Album, related_name="image_set", on_delete=models.CASCADE)
    media = models.FileField("이미지 파일", upload_to="worldcupapp/image/%Y/%m/%d/%h")
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)


class Gif(models.Model):
    album = models.ForeignKey(Album, related_name="gif_set", on_delete=models.CASCADE)
    media = models.FileField(
        "움짤 파일 (gif -> mp4)", upload_to="worldcupapp/gif/%Y/%m/%d/%h"
    )
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)


class Video(models.Model):
    album = models.ForeignKey(Album, related_name="video_set", on_delete=models.CASCADE)
    media = models.CharField("외부 비디오 링크", max_length=511)
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)


class Worldcup(models.Model):

    # TODO: A나 P로 전환할 경우 적합한 유효성 검사 필요.
    # A: album의 미디어 갯수가 2개 미만일 때
    # P: album의 미디어 갯수가 2개 미만일 때 + password에 대한 설정까지
    PUBLISH_TYPES = [
        ("A", "All, 전체공개"),
        ("P", "Password, 암호"),
        ("N", "Not Publish, 비공개"),
    ]

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

    publish_type = models.CharField(
        "배포 방식", max_length=1, choices=PUBLISH_TYPES, default="N"
    )

    password = models.CharField(
        "암호",
        blank=True,
        max_length=31,
        validators=[MinLengthValidator(1, "최소 한 글자 이상의 암호를 설정해주세요.")],
    )

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    play_count = models.PositiveIntegerField("플레이 횟수", default=0, editable=False)