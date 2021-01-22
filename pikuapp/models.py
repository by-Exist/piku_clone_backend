from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator


User = get_user_model()


# =================
# [ Mixin's Model ]
# =================


class TimeStempedModelMixin(models.Model):
    created_at = models.DateTimeField("생성시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정시각", auto_now=True)

    class Meta:
        abstract = True


# =================
# [ Album's Model ]
# =================


class Album(models.Model):
    thumbnail = models.ImageField(
        "썸네일", upload_to="worldcupapp/album/thumbnail/%Y/%m/%d/", blank=True
    )


# =================
# [ Media's Model ]
# =================


class AbstractMedia(TimeStempedModelMixin, models.Model):

    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    title = models.CharField("제목", max_length=31)
    win_count = models.PositiveIntegerField("월드컵 승리 횟수", editable=False, default=0)
    choice_count = models.PositiveIntegerField("1:1 승리 횟수", editable=False, default=0)

    class Meta:
        abstract = True


class Text(AbstractMedia):
    media = models.TextField("텍스트", max_length=511)


class Image(AbstractMedia):
    media = models.FileField("이미지 파일", upload_to="worldcupapp/image/%Y/%m/%d/%h")


# =======================
# [ MediaReport's Model ]
# =======================


class MediaReport(TimeStempedModelMixin, models.Model):

    REPORT_CATEGORY = [
        ("음란물", "음란물을 게시하였습니다."),
        ("기타", "기타"),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="신고자")
    worldcup = models.ForeignKey(
        "Worldcup",
        on_delete=models.CASCADE,
        verbose_name="신고된 미디어가 포함된 월드컵",
    )

    media_id = models.PositiveIntegerField("신고된 미디어 id")
    category = models.TextField("신고 사유", choices=REPORT_CATEGORY)
    contents = models.TextField("신고 내용", max_length=255, blank=True)


# ========================
# [ CommentBoard's Model ]
# ========================


class CommentBoard(models.Model):
    pass


# ===================
# [ Comment's Model ]
# ===================


class AbstractComment(TimeStempedModelMixin, models.Model):

    comment_board = models.ForeignKey(CommentBoard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    worldcup = models.ForeignKey(
        "Worldcup", on_delete=models.CASCADE, verbose_name="월드컵"
    )

    content = models.TextField("댓글 내용", max_length=511)

    class Meta:
        abstract = True


class TextComment(AbstractComment):
    media = models.ForeignKey(
        Text, on_delete=models.CASCADE, verbose_name="텍스트 미디어", null=True, blank=True
    )


class ImageComment(AbstractComment):
    media = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name="이미지 미디어", null=True, blank=True
    )


# =========================
# [ CommentReport's Model ]
# =========================


class CommentReport(TimeStempedModelMixin, models.Model):

    REPORT_CATEGORY = [
        ("욕설", "해당 댓글에 욕설이 포함되어 있습니다."),
        ("기타", "기타"),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="신고자")
    worldcup = models.ForeignKey(
        "Worldcup", on_delete=models.CASCADE, verbose_name="신고된 댓글이 포함된 월드컵"
    )

    comment_id = models.PositiveIntegerField("신고된 댓글 id")
    category = models.TextField("신고 사유", choices=REPORT_CATEGORY)
    contents = models.TextField("신고 내용", max_length=255, blank=True)


# ====================
# [ Worldcup's Model ]
# ====================


class Worldcup(TimeStempedModelMixin, models.Model):

    PUBLISH_TYPE = [
        ("A", "전체 공개"),
        ("P", "암호 공개"),
        ("N", "비공개"),
    ]

    MEDIA_TYPE = [
        ("T", "텍스트"),
        ("I", "이미지"),
    ]

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자", editable=False
    )
    album = models.OneToOneField(Album, on_delete=models.CASCADE, verbose_name="미디어")
    comment_board = models.OneToOneField(
        CommentBoard, on_delete=models.CASCADE, verbose_name="댓글"
    )

    title = models.CharField("제목", max_length=63)
    intro = models.CharField("소개", max_length=255)

    publish_type = models.CharField(
        "배포 방식", max_length=1, choices=PUBLISH_TYPE, default="N"
    )
    media_type = models.CharField(
        "미디어 타입", max_length=1, choices=MEDIA_TYPE, default="I"
    )

    password = models.CharField(
        "암호",
        blank=True,
        max_length=31,
        validators=[MinLengthValidator(3, "세 글자 이상의 암호를 설정해주세요.")],
    )
    play_count = models.PositiveIntegerField("플레이 횟수", default=0, editable=False)
