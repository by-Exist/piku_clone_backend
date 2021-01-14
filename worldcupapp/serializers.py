from dataclasses import fields
from tkinter import Text
from rest_framework import serializers
from . import models


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Text
        fields = ["media"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ["media"]


class GifSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gif
        fields = ["media"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ["media"]


# FIXME: Serializer의 어떤 동작 과정때문인지는 몰라도 media_list를 가져오기 위한 동작으로 추정되는 쿼리가 4번씩 반복된다. 가능하다면 수정.
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = [
            "media_type",
            "media_list",
        ]

    def get_media_serializer_class(album):
        media_types = {
            "T": TextSerializer,
            "I": ImageSerializer,
            "G": GifSerializer,
            "V": VideoSerializer,
        }
        return media_types[album.media_type]


class WorldcupUsedAlbumSerializer(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField("album-detail")

    class Meta:
        model = models.Album
        fields = ["media_type", "link"]


class WorldcupSerializer(serializers.ModelSerializer):

    creator = serializers.CharField(read_only=True, source="creator.profile.nickname")
    album = WorldcupUsedAlbumSerializer()

    class Meta:
        model = models.Worldcup
        fields = [
            "title",
            "intro",
            "creator",
            "created_at",
            "updated_at",
            "play_count",
            "album",
        ]

    def get_creator(self, worldcup):
        return worldcup.creator.nickname

    def create(self, validated_data):

        worldcup_data = validated_data
        worldcup_data["creator"] = self.context["request"].user

        album_data = validated_data.pop("album", None)

        worldcup = models.Worldcup.objects.create_with_album(
            worldcup_data,
            album_data,
        )
        return worldcup

    def update(self, instance, validated_data):

        worldcup = instance
        worldcup_data = validated_data
        worldcup_data["creator"] = self.context["request"].user

        album_data = validated_data.pop("album", None)

        worldcup = models.Worldcup.objects.update_with_album(
            worldcup,
            worldcup_data,
            album_data,
        )

        return worldcup