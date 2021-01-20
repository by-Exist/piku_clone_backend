from accountapp.policys import UserViewSetPolicy
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from accountapp import serializers as user_serializer


User = get_user_model()


# ===============
# [ User's View ]
# ===============


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile")
    serializer_class = user_serializer.UserSerializer
    permission_classes = [UserViewSetPolicy]

    def get_serializer_class(self):
        if self.action == "list":
            return user_serializer.UserListSerializer
        elif self.action == "create":
            return user_serializer.UserCreateSerializer
        elif self.action == "retrieve":
            return user_serializer.UserRetrieveSerializer
        elif self.action in ["update", "partial_update"]:
            return user_serializer.UserUpdateSerializer
        return super().get_serializer_class()