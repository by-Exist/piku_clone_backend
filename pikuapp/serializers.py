from accountapp.serializers import UserListSerializer, UserRetrieveSerializer
from pikuapp.models import (
    Text,
    Image,
    TextComment,
    ImageComment,
    CommentBoard,
    Album,
    Worldcup,
)
from rest_framework import serializers


# =====================
# [ Text's Serializer ]
# =====================


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class TextListSerializer(TextSerializer):
    class Meta:
        model = Text
        fields = ["id", "title", "media"]


class TextCreateSerializer(TextSerializer):
    class Meta:
        model = Text
        fields = ["title", "media"]


# ======================
# [ Image's Serializer ]
# ======================


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ImageListSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "media"]


class ImageCreateSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ["title", "media"]


# ============================
# [ TextComment's Serializer ]
# ============================


class TextCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextComment
        fields = "__all__"


class TextCommentListSerializer(TextCommentSerializer):

    nickname = serializers.CharField(source="user.profile.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")
    media = serializers.CharField(source="media.media")

    class Meta:
        model = TextComment
        fields = ["id", "content", "media", "nickname", "avatar"]


class TextCommentCreateSerializer(TextCommentSerializer):

    media_id = serializers.IntegerField(required=False)

    class Meta:
        model = TextComment
        fields = ["media_id", "content"]

    def validate_media_id(self, media_id):
        worldcup = Worldcup.objects.get(pk=self.context["view"].kwargs["worldcup_pk"])
        if media_id not in worldcup.album.media_set.values_list("id", flat=True):
            raise serializers.ValidationError(
                {"media_id": "월드컵에 사용된 미디어에 해당 id를 지닌 미디어가 존재하지 않습니다."}
            )
        return media_id


# =============================
# [ ImageComment's Serializer ]
# =============================


class ImageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComment
        fields = "__all__"


class ImageCommentListSerializer(ImageCommentSerializer):

    nickname = serializers.CharField(source="user.profile.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")
    media = serializers.ImageField(source="media.media")

    class Meta:
        model = ImageComment
        fields = ["id", "content", "media", "nickname", "avatar"]


class ImageCommentCreateSerializer(ImageCommentSerializer):

    media_id = serializers.IntegerField()

    class Meta:
        model = ImageComment
        fields = "media_id", "content"

    def validate_media_id(self, media_id):
        worldcup = self.context["worldcup"]
        if media_id not in worldcup.album.media_set.values_list("id", flat=True):
            raise serializers.ValidationError(
                {"media_id": "월드컵에 사용된 미디어에 해당 id를 지닌 미디어가 존재하지 않습니다."}
            )
        return media_id


# =========================
# [ Worldcup's Serializer ]
#
# fields = [
#     "id",
#     "album",
#     "creator",
#     "comment_board",
#     "title",
#     "intro",
#     "publish_type",
#     "media_type",
#     "password",
#     "created_at",
#     "updated_at",
#     "play_count",
# ]
# =========================


class WorldcupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Worldcup
        fields = "__all__"


class WorldcupListSerializer(WorldcupSerializer):

    thumbnail = serializers.ImageField(source="album.thumbnail")

    class Meta:
        model = Worldcup
        fields = ["id", "url", "thumbnail", "title", "intro", "media_type"]


class WorldcupCreateSerializer(WorldcupSerializer):
    class Meta:
        model = Worldcup
        fields = [
            "id",
            "url",
            "title",
            "intro",
            "media_type",
        ]


class WorldcupRetrieveSerializer(WorldcupSerializer):

    medias = serializers.HyperlinkedIdentityField(
        view_name="media-list", lookup_url_kwarg="worldcup_pk"
    )
    comments = serializers.HyperlinkedIdentityField(
        view_name="comment-list", lookup_url_kwarg="worldcup_pk"
    )
    thumbnail = serializers.ImageField(source="album.thumbnail")
    creator = UserListSerializer()

    class Meta:
        model = Worldcup
        fields = [
            "id",
            "thumbnail",
            "title",
            "intro",
            "creator",
            "publish_type",
            "media_type",
            "created_at",
            "updated_at",
            "play_count",
            "medias",
            "comments",
        ]


class WorldcupUpdateSerializer(WorldcupSerializer):
    class Meta:
        model = Worldcup
        fields = [
            "title",
            "intro",
            "media_type",
            "publish_type",
            "password",
        ]
        extra_kwargs = {
            "password": {
                "style": {"input_type": "password"},
                "write_only": True,
            },
        }

    def validate(self, attrs):
        publish_type = attrs.get("publish_type", None)
        password = attrs.get("password", None)
        if publish_type == "P" and not password:
            raise serializers.ValidationError({"password": "해당 월드컵의 암호를 지정해주세요."})
        return attrs