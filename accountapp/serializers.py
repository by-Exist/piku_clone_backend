from django.contrib.auth import get_user_model
from rest_framework import serializers
from accountapp.models import Profile


User = get_user_model()


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
        fields = ["id", "avatar"]


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class ProfilePartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


# =====================
# [ User's Serializer ]
#
# fields = [
#     id,
#     password,
#     last_login,
#     is_superuser,
#     username,
#     first_name,
#     last_name,
#     email,
#     is_staff,
#     is_active,
#     date_joined,
#     groups,
#     user_permissions,
# ]
# =====================


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(UserSerializer):

    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = User
        fields = ["id", "url", "nickname", "avatar"]


class UserCreateSerializer(UserSerializer):

    profile = ProfileCreateSerializer()

    class Meta:
        model = User
        fields = ["username", "nickname", "password", "profile"]
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        profile_validated_data = validated_data.pop("profile", None)
        user = User.objects.create_user(**validated_data)
        if profile_validated_data:
            Profile.objects.create(user=user, **profile_validated_data)
        return user


class UserRetrieveSerializer(UserSerializer):

    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar", "date_joined"]


class UserUpdateSerializer(UserSerializer):

    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ["nickname", "password", "profile"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            }
        }

    def update(self, user, validated_data):
        profile_validated_data = validated_data.pop("profile", {})
        if not hasattr(user, "profile"):
            Profile.objects.create(user=user)
        profile = user.profile
        for key, value in profile_validated_data.items():
            setattr(profile, key, value)
        profile.save()
        for key, value in validated_data.items():
            if key != "password":
                setattr(user, key, value)
            else:
                user.set_password(value)
        user.save()
        return user