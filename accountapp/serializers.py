from accountapp.models import Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar", "nickname"]


class UserSerializer(serializers.ModelSerializer):

    # 중첩 필드에 대한 객체 생성은 그 동작이 모호하기 때문에 직접 create 메서드를 지정해주어야 한다.
    profile = ProfileSerializer()

    # profile로 serializer를 중첩하지 않고 'nickname', 'avatar' 필드를 추가할 수 있겠지만
    # source="profile.nickname" 등의 방식으로 연동한다 해도 validator가 사라진다.
    # 이것만 해결할 수 있다면 굳이 중첩을 사용하지는 않을텐데.

    class Meta:
        model = User
        fields = ["username", "password", "profile"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # 모든 데이터 변경을 요구하는 작업은 Model의 메서드나 Model Manager를 통해 이루어지도록 하자.
    # https://www.dabapps.com/blog/django-models-and-encapsulation/
    def create(self, validated_data):
        user = User.objects.create_with_profile(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance = User.objects.update_with_profile(instance, **validated_data)
        return instance