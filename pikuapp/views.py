from pikuapp.serializers import (
    ImageCommentCreateSerializer,
    ImageCreateSerializer,
    ImageListSerializer,
    TextCommentCreateSerializer,
    TextCreateSerializer,
    TextListSerializer,
    TextCommentSerializer,
    ImageCommentSerializer,
    WorldcupCreateSerializer,
    WorldcupListSerializer,
    WorldcupRetrieveSerializer,
    WorldcupSerializer,
    WorldcupUpdateSerializer,
)
from pikuapp.models import (
    Text,
    Image,
    Album,
    TextComment,
    ImageComment,
    CommentBoard,
    Worldcup,
)
from rest_framework import viewsets


class MediaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        album = worldcup.album
        media_type = worldcup.media_type
        if media_type == "T":
            return Text.objects.filter(album=album)
        elif media_type == "I":
            return Image.objects.filter(album=album)
        return super().get_queryset()

    def get_serializer_class(self, *args, **kwargs):
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        media_type = worldcup.media_type
        if self.action == "list":
            if media_type == "T":
                return TextListSerializer
            elif media_type == "I":
                return ImageListSerializer
        elif self.action == "create":
            if media_type == "T":
                return TextCreateSerializer
            elif media_type == "I":
                return ImageCreateSerializer
        return super().get_serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        album = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"]).album
        serializer.save(album=album)


class CommentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        comment_board = worldcup.comment_board
        media_type = worldcup.media_type
        if media_type == "T":
            return TextComment.objects.filter(comment_board=comment_board)
        elif media_type == "I":
            return ImageComment.objects.filter(comment_board=comment_board)
        return super().get_queryset()

    def get_serializer_class(self, *args, **kwargs):
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        media_type = worldcup.media_type
        if self.action == "create":
            if media_type == "T":
                return TextCommentCreateSerializer
            elif media_type == "I":
                return ImageCommentCreateSerializer
        if media_type == "T":
            return TextCommentSerializer
        elif media_type == "I":
            return ImageCommentSerializer
        return super().get_serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        comment_board = worldcup.comment_board
        user = self.request.user
        media = self.kwargs.get("media_id", None)
        serializer.save(
            worldcup=worldcup, comment_board=comment_board, media=media, user=user
        )


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = Worldcup.objects.all()
    serializer_class = WorldcupSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return WorldcupListSerializer
        elif self.action == "create":
            return WorldcupCreateSerializer
        elif self.action == "retrieve":
            return WorldcupRetrieveSerializer
        elif self.action in ["update", "partial_update"]:
            return WorldcupUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        album = Album.objects.create()
        comment_board = CommentBoard.objects.create()
        creator = self.request.user
        serializer.save(album=album, comment_board=comment_board, creator=creator)
