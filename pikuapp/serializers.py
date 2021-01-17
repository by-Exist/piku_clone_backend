from accountapp.serializers import UserListSerializer, UserRetrieveSerializer
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


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "thumbnail"]


class AlbumRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


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

    media_id = serializers.IntegerField()

    class Meta:
        model = TextComment
        fields = ["media_id", "content"]

    def validate_media_id(self, media_id):
        worldcup = self.context["worldcup"]
        if media_id not in worldcup.album.media_set.values_list("id", flat=True):
            raise serializers.ValidationError(
                {"media_id": "월드컵에 사용된 미디어에 해당 id를 지닌 미디어가 존재하지 않습니다."}
            )
        return media_id

    def create(self, validated_data):
        worldcup = self.context["worldcup"]
        comment = worldcup.comment
        user = self.context["request"].user
        media = worldcup.album.media_set.get(id=validated_data["media_id"])
        data = {
            "comment": comment,
            "user": user,
            "worldcup": worldcup,
            "media": media,
            "content": validated_data["content"],
        }
        comment = TextComment.objects.create(**data)
        return comment


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

    def create(self, validated_data):
        worldcup = self.context["worldcup"]
        comment = worldcup.comment
        user = self.context["request"].user
        media = worldcup.album.media_set.get(id=validated_data["media_id"])
        data = {
            "comment": comment,
            "user": user,
            "worldcup": worldcup,
            "media": media,
            "content": validated_data["content"],
        }
        comment = ImageComment.objects.create(**data)
        return comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class WorldcupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worldcup
        fields = "__all__"


class WorldcupListSerializer(WorldcupSerializer):

    thumbnail = serializers.ImageField(source="album.thumbnail")

    class Meta:
        model = Worldcup
        fields = ["id", "thumbnail", "title", "intro", "media_type"]


class WorldcupCreateSerializer(WorldcupSerializer):
    class Meta:
        model = Worldcup
        fields = [
            "title",
            "intro",
            "media_type",
        ]

    def create(self, validated_data):
        album = Album.objects.create()
        comment = Comment.objects.create()
        creator = self.context["request"].user
        validated_data |= {"album": album, "comment": comment, "creator": creator}
        worldcup = Worldcup.objects.create(**validated_data)
        return worldcup


class WorldcupRetrieveSerializer(WorldcupSerializer):

    thumbnail = serializers.ImageField(source="album.thumbnail")
    creator = UserListSerializer()

    class Meta:
        model = Worldcup
        fields = "__all__"
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

    # TODO: https://www.django-rest-framework.org/api-guide/serializers/#partial-updates 참조
    def update(self, worldcup, validated_data):
        fields = ["title", "intro", "media_type", "publish_type", "password"]
        # FIXME: 해당 필드의 기본값을 찾아오는 방법이 분명 있을 것 같은데...
        defaults = ["", "", "I", "N", ""]
        for field, default in zip(fields, defaults):
            if field in validated_data:
                setattr(worldcup, field, validated_data[field])
            else:
                setattr(worldcup, field, default)
        worldcup.save()
        return worldcup


class WorldcupPartialUpdateSerializer(WorldcupSerializer):
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

    # TODO: https://www.django-rest-framework.org/api-guide/serializers/#partial-updates 참조
    def update(self, worldcup, validated_data):
        fields = ["title", "intro", "media_type", "publish_type", "password"]
        for field in fields:
            if field in validated_data:
                setattr(worldcup, field, validated_data[field])
        worldcup.save()
        return worldcup
        # patch - 필드가 너무 많을 때 (검증 안됨)
        # for field in self._writable_fields:
        #     if field.field_name in validated_data:
        #         setattr(worldcup, field, validated_data[field])
        # worldcup.save()
        # return worldcup