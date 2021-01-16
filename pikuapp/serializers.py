from pikuapp.models import (
    Text,
    Image,
    Album,
    TextComment,
    ImageComment,
    Comment,
    Worldcup,
)
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class TextCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextComment
        fields = "__all__"


class ImageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class WorldcupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worldcup
        fields = "__all__"