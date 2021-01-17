from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from accountapp.models import Profile


# ========================
# [ Profile's Serializer ]
# ========================


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "nickname", "avatar"]


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data |= {"user": user}
        profile = Profile.objects.create(**validated_data)
        return profile


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]

    def update(self, profile, validated_data):
        print(validated_data)
        nickname = validated_data.get("nickname", "")
        avatar = validated_data.get("avatar", "")
        profile.nickname = nickname
        profile.avatar = avatar
        profile.save()
        return profile


class ProfilePartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]

    def update(self, profile, validated_data):
        nickname = validated_data.get("nickname", None)
        avatar = validated_data.get("avatar", None)
        if nickname:
            profile.nickname = nickname
        if avatar:
            profile.avatar = avatar
        profile.save()
        return profile


# =====================
# [ User's Serializer ]
# required - id, password
# other - last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, groups, user_permissions
# =====================


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(UserSerializer):

    nickname = serializers.CharField(source="profile.nickname")
    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = User
        fields = ["id", "nickname", "avatar"]


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user = User.objects.create_user(username=username, password=password)
        return user


class UserRetrieveSerializer(UserSerializer):

    nickname = serializers.CharField(source="profile.nickname")
    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar", "date_joined"]


class UserUpdateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["password"]
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
            }
        }

    def update(self, user, validated_data):
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user


class UserPartialUpdateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["password"]
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
            }
        }

    def update(self, user, validated_data):
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user