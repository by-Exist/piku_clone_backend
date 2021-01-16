from worldcupapp.models import Album, Gif, Image, Text, Video, Worldcup
from rest_framework import serializers


# =====================
# [ Text's Serializer ]
# =====================


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class TextCreateSerializer(TextSerializer):
    class Meta:
        model = Text
        fields = ["media"]


# ======================
# [ Image's Serializer ]
# ======================


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ImageCreateSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ["media"]


# =====================
# [ Gif's Serializer ]
# =====================


class GifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gif
        fields = "__all__"


class GifCreateSerializer(GifSerializer):
    class Meta:
        model = Gif
        fields = ["media"]


# =====================
# [ Video's Serializer ]
# =====================


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VideoCreateSerializer(VideoSerializer):
    class Meta:
        model = Video
        fields = ["media"]


# ======================
# [ Media's Serializer ]
# ======================


class MediaWinCountSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class MediaChoiceCountsSerializer(serializers.Serializer):
    pk_list = serializers.ListField()


class MediaListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    media = serializers.CharField()


class MediaScoreboardSerializer(serializers.Serializer):
    media = serializers.CharField()
    win_count = serializers.IntegerField()
    choice_count = serializers.IntegerField()


# ======================
# [ Album's Serializer ]
# ======================


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class AlbumListSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["id", "thumbnail"]


class AlbumCreateSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["media_type"]


class AlbumRetrieveSerializer(AlbumSerializer):

    media_set = MediaListSerializer(many=True)

    class Meta:
        model = Album
        fields = ["id", "media_type", "thumbnail", "media_set"]


class AlbumUpdateWithPartialUpdateSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["media_type"]


# =========================
# [ Worldcup's Serializer ]
# =========================


class WorldcupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worldcup
        fields = "__all__"


class WorldcupListSerializer(WorldcupSerializer):

    album = AlbumListSerializer()

    class Meta:
        model = Worldcup
        fields = ["id", "title", "intro", "album"]


class WorldcupCreateSerializer(WorldcupSerializer):

    album = AlbumCreateSerializer()

    class Meta:
        model = Worldcup
        fields = ["title", "intro", "album"]

    def create(self, validated_data):
        user = self.context["request"].user
        album_data = validated_data.pop("album")
        album = Album.objects.create(**album_data)
        worldcup = Worldcup.objects.create(album=album, creator=user, **validated_data)
        return worldcup


class WorldcupRetrieveSerializer(WorldcupSerializer):

    album = AlbumRetrieveSerializer()
    creator = serializers.CharField(source="creator.profile.nickname", read_only=True)

    class Meta:
        model = Worldcup
        fields = [
            "id",
            "title",
            "intro",
            "creator",
            "created_at",
            "updated_at",
            "play_count",
            "album",
        ]


class WorldcupUpdateWithPartialUpdateSerializer(WorldcupSerializer):

    album = AlbumUpdateWithPartialUpdateSerializer()

    class Meta:
        model = Worldcup
        fields = ["title", "intro", "publish_type", "password", "album"]
        # extra_kwargs = {"password": {"write_only": True}}

    def validate(self, fields):
        album = self.context["album"]
        if (
            (fields.get("publish_type", None))
            and (fields["publish_type"] in ["A", "P"])
            and (len(album.media_list) < 2)
        ):
            raise serializers.ValidationError(
                {"publish_type": "월드컵을 공개하기 위해서는 최소 두 개 이상의 미디어가 포함되어 있어야 합니다."}
            )
        if (fields.get("publish_type") != "P") and ("password" in fields):
            fields.pop("password")
        return fields

    def update(self, worldcup, validated_data):
        album = worldcup.album
        album_data = validated_data.pop("album")
        for key, value in album_data.items():
            setattr(album, key, value)
        album.save(update_fields=[*album_data.keys()])
        for key, value in validated_data.items():
            setattr(worldcup, key, value)
        worldcup.save(update_fields=[*validated_data.keys()])
        return worldcup