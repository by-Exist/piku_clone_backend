from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# ================
# [ User's Model ]
# ================


class CustomUserManager(UserManager):
    def create_with_profile(self, **kwargs):
        user = User(username=kwargs["username"])
        user.set_password(kwargs["password"])
        user.save()
        profile = Profile(
            user=user,
            nickname=kwargs["profile"]["nickname"],
            avatar=kwargs["profile"].get("avatar", None),
        )
        profile.save()
        return user

    def update_with_profile(self, user, **kwargs):
        if "password" in kwargs:
            user.set_password(kwargs["password"])
            user.save()
        if "profile" in kwargs:
            profile = user.profile
            data = kwargs["profile"]
            profile.nickname = data.get("nickname", profile.nickname)
            profile.avatar = data.get("avatar", profile.avatar)
            profile.save()
        return user


class User(AbstractUser):

    objects = CustomUserManager()


# ===================
# [ Profile's Model ]
# ===================


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="유저",
    )

    nickname = models.CharField(
        "닉네임",
        max_length=12,
        unique=True,
        validators=[
            MinLengthValidator(3, "세 글자 이상 입력해주세요."),
            RegexValidator(r"^[가-힣a-zA-Z]+$", "알파벳과 한글로 작성해주세요. (단일 자음 모음 및 공백 불가)"),
        ],
    )
    avatar = models.ImageField(
        "아바타 이미지", upload_to="accountapp/profile/avatar/%Y/%m/%d", blank=True
    )