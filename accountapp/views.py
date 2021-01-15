from django.contrib.auth import get_user_model
from rest_framework import viewsets
from accountapp import serializers

# from rest_framework_jwt.views import obtain_jwt_token
from . import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().select_related("profile")
    serializer_class = serializers.UserSerializer
