from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# ================
# [ User's Model ]
# ================


class User(AbstractUser):
    pass


# ===================
# [ Profile's Model ]
# ===================


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="유저")

    avatar = models.ImageField(
        "아바타 이미지", upload_to="accountapp/profile/avatar/%Y/%m/%d", blank=True
    )
    nickname = models.CharField(
        "닉네임",
        max_length=12,
        unique=True,
        validators=[
            MinLengthValidator(3, "세 글자 이상 입력해주세요."),
            RegexValidator(
                r"^[a-zA-Z0-9가-힣_]+$", "알파벳, 숫자, 한글, 특수기호(_)로 구성된 닉네임을 입력해주세요."
            ),
        ],
    )