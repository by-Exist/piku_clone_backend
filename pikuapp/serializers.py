from django.shortcuts import get_object_or_404
from django.urls import reverse
from accountapp.serializers import UserListSerializer
from pikuapp.models import (
    Album,
    CommentBoard,
    CommentReport,
    MediaReport,
    Text,
    Image,
    TextComment,
    ImageComment,
    Worldcup,
)
from rest_framework import serializers


# TODO: Abstract MediaSerializer 또는 CommentSerializer들을 만든 뒤
# 하위 미디어 시리얼라이저에서 상속만으로 활용할 수도 있겠다.


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

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        album = Worldcup.objects.get(pk=worldcup_pk).album
        validated_data |= {"album": album}
        return super().create(validated_data)


class TextRetrieveSerializer(TextSerializer):
    class Meta:
        model = Text
        fields = ["id", "title", "media"]


class TextUpdateSerializer(TextSerializer):
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

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        album = Worldcup.objects.get(pk=worldcup_pk).album
        validated_data |= {"album": album}
        return super().create(validated_data)


class ImageRetrieveSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "media"]


class ImageUpdateSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ["title", "media"]


# ============================
# [ MediaReport's Serializer ]
# ============================


class MediaReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MediaReport
        fields = "__all__"

    def get_media_url(self, obj):
        url = reverse("media-detail", args=[obj.worldcup.pk, obj.media_id])
        return self.context["request"].build_absolute_uri(url)


class MediaReportListSerializer(MediaReportSerializer):

    media_url = serializers.SerializerMethodField("get_media_url")

    class Meta:
        model = MediaReport
        fields = [
            "id",
            "url",
            "worldcup",
            "media_url",
            "reporter",
            "category",
            "contents",
        ]


class MediaReportCreateSerializer(MediaReportSerializer):

    worldcup_id = serializers.IntegerField()

    class Meta:
        model = MediaReport
        fields = ["worldcup_id", "media_id", "category", "contents"]

    def validate(self, attrs):
        worldcup = get_object_or_404(Worldcup, pk=attrs["worldcup_id"])
        MEDIA_TYPES = {
            "T": Text,
            "I": Image,
        }
        media_ids = (
            MEDIA_TYPES[worldcup.media_type]
            .objects.filter(album=worldcup.album)
            .values_list("id", flat=True)
        )
        if not attrs["media_id"] in media_ids:
            raise serializers.ValidationError({"media_id": "해당 월드컵에 미디어가 존재하지 않습니다."})
        return attrs

    def create(self, validated_data):
        reporter = self.context["request"].user
        worldcup = get_object_or_404(Worldcup, pk=validated_data.pop("worldcup_id"))
        validated_data |= {
            "reporter": reporter,
            "worldcup": worldcup,
        }
        return super().create(validated_data)


class MediaReportRetrieveSerializer(MediaReportSerializer):

    media_url = serializers.SerializerMethodField("get_media_url")

    class Meta:
        model = MediaReport
        fields = [
            "worldcup",
            "media_url",
            "reporter",
            "category",
            "contents",
            "created_at",
            "updated_at",
        ]


# ============================
# [ TextComment's Serializer ]
# ============================


class TextCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextComment
        fields = "__all__"

    def get_url(self, obj):
        url = reverse("comment-detail", args=[obj.worldcup.pk, obj.pk])
        return self.context["request"].build_absolute_uri(url)


class TextCommentListSerializer(TextCommentSerializer):

    nickname = serializers.CharField(source="user.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")
    url = serializers.SerializerMethodField("get_url")

    class Meta:
        model = TextComment
        fields = [
            "id",
            "url",
            "content",
            "media",
            "nickname",
            "avatar",
            "created_at",
            "updated_at",
        ]


class TextCommentCreateSerializer(TextCommentSerializer):

    media_id = serializers.IntegerField(required=False)

    class Meta:
        model = TextComment
        fields = ["media_id", "content"]

    def validate_media_id(self, media_id):
        if not self.context["view"].get_queryset().filter(id=media_id).exists():
            raise serializers.ValidationError(
                {"media_id": "월드컵에 사용된 미디어에 해당 id를 지닌 미디어가 존재하지 않습니다."}
            )
        return media_id

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        worldcup = Worldcup.objects.get(pk=worldcup_pk)
        comment_board = worldcup.comment_board
        user = self.context["request"].user
        media = self.context["view"].kwargs.get("media_id", None)
        validated_data |= {
            "worldcup": worldcup,
            "comment_board": comment_board,
            "media": media,
            "user": user,
        }
        return super().create(validated_data)


class TextCommentRetrieveSerializer(TextCommentSerializer):

    nickname = serializers.CharField(source="user.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")

    class Meta:
        model = TextComment
        fields = ["id", "content", "media", "nickname", "avatar"]


class TextCommentUpdateSerializer(TextCommentSerializer):
    class Meta:
        model = TextComment
        fields = ["content"]


# =============================
# [ ImageComment's Serializer ]
# =============================


class ImageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComment
        fields = "__all__"

    def get_url(self, obj):
        url = reverse("comment-detail", args=[obj.worldcup.pk, obj.pk])
        return self.context["request"].build_absolute_uri(url)


class ImageCommentListSerializer(ImageCommentSerializer):

    nickname = serializers.CharField(source="user.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")
    url = serializers.SerializerMethodField("get_url")

    class Meta:
        model = ImageComment
        fields = [
            "id",
            "url",
            "content",
            "media",
            "nickname",
            "avatar",
            "created_at",
            "updated_at",
        ]


class ImageCommentCreateSerializer(ImageCommentSerializer):

    media_id = serializers.IntegerField()

    class Meta:
        model = ImageComment
        fields = "media_id", "content"

    # FIXME: album의 media_set 프로퍼티를 활용해야 하나?
    # def validate_media_id(self, media_id):
    #     worldcup = self.context["worldcup"]
    #     if media_id not in worldcup.album.media_set.values_list("id", flat=True):
    #         raise serializers.ValidationError(
    #             {"media_id": "월드컵에 사용된 미디어에 해당 id를 지닌 미디어가 존재하지 않습니다."}
    #         )
    #     return media_id

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        worldcup = Worldcup.objects.get(pk=worldcup_pk)
        comment_board = worldcup.comment_board
        user = self.context["request"].user
        media = self.context["view"].kwargs.get("media_id", None)
        validated_data |= {
            "worldcup": worldcup,
            "comment_board": comment_board,
            "media": media,
            "user": user,
        }
        return super().create(validated_data)


class ImageCommentRetrieveSerializer(ImageCommentSerializer):

    nickname = serializers.CharField(source="user.nickname")
    avatar = serializers.ImageField(source="user.profile.avatar")

    class Meta:
        model = ImageComment
        fields = ["id", "content", "media", "nickname", "avatar"]


class ImageCommentUpdateSerializer(ImageCommentSerializer):
    class Meta:
        model = ImageComment
        fields = ["content"]


# ==============================
# [ CommentReport's Serializer ]
# ==============================


class CommentReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommentReport
        fields = "__all__"

    def get_comment_url(self, obj):
        url = reverse("comment-detail", args=[obj.worldcup.pk, obj.comment_id])
        return self.context["request"].build_absolute_uri(url)


class CommentReportListSerializer(CommentReportSerializer):

    comment_url = serializers.SerializerMethodField("get_comment_url")

    class Meta:
        model = CommentReport
        fields = [
            "id",
            "url",
            "worldcup",
            "comment_url",
            "reporter",
            "category",
            "contents",
        ]


class CommentReportCreateSerializer(CommentReportSerializer):

    worldcup_id = serializers.IntegerField()

    class Meta:
        model = CommentReport
        fields = ["worldcup_id", "comment_id", "category", "contents"]

    def validate(self, attrs):
        worldcup = get_object_or_404(Worldcup, pk=attrs["worldcup_id"])
        MEDIA_TYPES = {
            "T": TextComment,
            "I": ImageComment,
        }
        comment_ids = (
            MEDIA_TYPES[worldcup.media_type]
            .objects.filter(comment_board=worldcup.comment_board)
            .values_list("id", flat=True)
        )
        if not attrs["comment_id"] in comment_ids:
            raise serializers.ValidationError({"comment_id": "해당 월드컵에 댓글이 존재하지 않습니다."})
        return attrs

    def create(self, validated_data):
        reporter = self.context["request"].user
        worldcup = get_object_or_404(Worldcup, pk=validated_data.pop("worldcup_id"))
        validated_data |= {
            "reporter": reporter,
            "worldcup": worldcup,
        }
        return super().create(validated_data)


class CommentReportRetrieveSerializer(CommentReportSerializer):

    comment_url = serializers.SerializerMethodField("get_comment_url")

    class Meta:
        model = CommentReport
        fields = [
            "worldcup",
            "comment_url",
            "reporter",
            "category",
            "contents",
            "created_at",
            "updated_at",
        ]


# =========================
# [ Worldcup's Serializer ]
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

    def create(self, validated_data):
        album = Album.objects.create()
        comment_board = CommentBoard.objects.create()
        creator = self.context["request"].user
        validated_data |= {
            "album": album,
            "comment_board": comment_board,
            "creator": creator,
        }
        return super().create(validated_data)


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
            raise serializers.ValidationError({"password": "암호 공개를 할 경우 암호가 필요합니다."})
        return attrs