from django.contrib.auth import get_user_model
from rest_framework import viewsets
from accountapp.models import Profile
from accountapp.serializers import UserSerializer, ProfileSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer