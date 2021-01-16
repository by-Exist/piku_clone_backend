from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator


User = get_user_model()


# =================
# [ Album's Model ]
# =================


class Album(models.Model):
    class MEDIA_TYPE(models.TextChoices):
        TEXT = "T", _("텍스트")
        IMAGE = "I", _("이미지")

    media_type = models.CharField("미디어 타입", choices=MEDIA_TYPE.choices)
    thumbnail = models.ImageField(
        "썸네일", upload_to="worldcupapp/album/thumbnail/%Y/%m/%d/", blank=True
    )


class AbstractMedia(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    title = models.CharField("이미지 제목", max_length=31)
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)

    class Meta:
        abstract = True


class Text(AbstractMedia):
    media = models.FileField("이미지 파일", upload_to="worldcupapp/image/%Y/%m/%d/%h")


class Image(AbstractMedia):
    media = models.FileField("이미지 파일", upload_to="worldcupapp/image/%Y/%m/%d/%h")


# ===================
# [ Comment's Model ]
# ===================


class Comment(models.Model):
    class WORLDCUP_TYPE(models.TextChoices):
        IMAGE = "I", _("이미지")

    worldcup_type = models.CharField()


class AbstractComment(models.Model):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    worldcup = models.ForeignKey(
        "Worldcup", on_delete=models.CASCADE, verbose_name="월드컵"
    )

    class Meta:
        abstract = True


class TextComment(AbstractComment):
    text = models.ForeignKey(Text, on_delete=models.CASCADE, verbose_name="댓글을 달 텍스트")
    content = models.TextField("댓글 내용", max_length=511)


class ImageComment(AbstractComment):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="댓글을 달 이미지")
    content = models.TextField("댓글 내용", max_length=511)


# ====================
# [ Worldcup's Model ]
# ====================


class Worldcup(models.Model):
    class PUBLISH_TYPE(models.TextChoices):
        All = "A", _("전체 공개")
        PASSWORD = "P", _("암호 공개")
        NO = "N", _("비공개")

    class MEDIA_TYPE(models.TextChoices):
        TEXT = "T", _("텍스트")
        IMAGE = "I", _("이미지")

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자", editable=False
    )
    album = models.OneToOneField(Album, on_delete=models.CASCADE, verbose_name="미디어")
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, verbose_name="댓글")

    title = models.CharField("제목", max_length=63)
    intro = models.CharField("소개", max_length=255)

    publish_type = models.CharField(
        "배포 방식", max_length=1, choices=PUBLISH_TYPE.choices, default=PUBLISH_TYPE.NO
    )
    media_type = models.CharField(
        "미디어 타입", max_length=1, choices=MEDIA_TYPE.choices, default=MEDIA_TYPE.IMAGE
    )

    password = models.CharField(
        "암호",
        blank=True,
        max_length=31,
        validators=[MinLengthValidator(3, "세 글자 이상의 암호를 설정해주세요.")],
    )

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    play_count = models.PositiveIntegerField("플레이 횟수", default=0, editable=False)
