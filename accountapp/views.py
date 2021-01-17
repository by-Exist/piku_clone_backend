from django.contrib.auth import get_user_model
from rest_framework import viewsets
from accountapp.models import Profile
from accountapp.serializers import (
    ProfileCreateSerializer,
    ProfileListSerializer,
    ProfilePartialUpdateSerializer,
    ProfileUpdateSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserPartialUpdateSerializer,
    UserRetrieveSerializer,
    UserSerializer,
    ProfileSerializer,
    UserUpdateSerializer,
)


User = get_user_model()


# [avatar, nickname, user]
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "create":
            return ProfileCreateSerializer
        elif self.action == "retrieve":
            return ProfileCreateSerializer
        elif self.action == "update":
            return ProfileUpdateSerializer
        elif self.action == "partial_update":
            return ProfilePartialUpdateSerializer
        return super().get_serializer_class()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        elif self.action == "create":
            return UserCreateSerializer
        elif self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "update":
            return UserUpdateSerializer
        elif self.action == "partial_update":
            return UserPartialUpdateSerializer
        return super().get_serializer_class()