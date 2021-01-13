from accountapp import serializers
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from . import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("profile")
    serializer_class = serializers.UserSerializer