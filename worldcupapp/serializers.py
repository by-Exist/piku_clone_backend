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
# [ Album's Serializer ]
# ======================


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"

    # FIXME: 아래의 두 스태틱 메서드는 어느 위치에 있는가 가장 적절할까?
    @staticmethod
    def get_media_list(album):
        for T, typ in album.MEDIA_TYPES:
            if T == album.media_type:
                data = getattr(album, f"{typ}_set").values_list("id", "media")
                # data = getattr(album, f"{typ}_set").values_list(
                #     "id", "media", "win_count", "choice_count"
                # )  # media win_count와 choice_count 테스트용
                return data
        return []

    @staticmethod
    def get_media_serializer_class(album):
        MEDIA_TYPES = {
            "T": TextCreateSerializer,
            "I": ImageCreateSerializer,
            "G": GifCreateSerializer,
            "V": VideoCreateSerializer,
        }
        return MEDIA_TYPES[album.media_type]


class AlbumListSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["id", "thumbnail"]


class AlbumCreateSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["media_type"]


class AlbumRetrieveSerializer(AlbumSerializer):

    media_list = serializers.SerializerMethodField("get_media_list")

    class Meta:
        model = Album
        fields = ["id", "media_type", "thumbnail", "media_list"]


class AlbumUpdateSerializer(AlbumSerializer):
    class Meta:
        model = Album
        fields = ["media_type"]


# =========================
# [ Worldcup's Serializer ]
# =========================


# TODO: 이제 validate 함수와 validate_data 함수를 잔뜩 만들어보자.


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
        fields = ["title", "intro", "publish_type", "password", "album"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        album_data = validated_data.pop("album")
        album = Album.objects.create(**album_data)
        worldcup = Worldcup.objects.create(album=album, creator=user, **validated_data)
        return worldcup

    def validate(self, attrs):
        if attrs["publish_type"] == "P":
            if not attrs["password"]:
                raise serializers.ValidationError({"password": "비밀번호를 설정해주세요."})
        return super().validate(attrs)


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


class WorldcupUpdateSerializer(WorldcupSerializer):

    album = AlbumUpdateSerializer()

    class Meta:
        model = Worldcup
        fields = ["title", "intro", "publish_type", "password", "album"]


class MediaWinCountSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class MediaChoiceCountsSerializer(serializers.Serializer):
    pk_list = serializers.ListField()
