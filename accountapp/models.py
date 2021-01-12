from zoneinfo import available_timezones
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class User(AbstractUser):
    pass


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="유저",
    )

    nickname = models.CharField(
        "닉네임",
        max_length=12,
        validators=[
            MinLengthValidator(3, "세 글자 이상 입력해주세요."),
            RegexValidator(r"^[가-힣a-zA-Z]+$", "알파벳과 한글(단일 자음 모음 불가)로 작성해주세요."),
        ],
    )

    avatar = models.ImageField(
        "아바타 이미지", upload_to="accountapp/profile/avatar/%Y/%m/%d", blank=True
    )
