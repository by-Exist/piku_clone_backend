from accountapp import serializers
from pikuapp.serializers import (
    CommentReportCreateSerializer,
    CommentReportListSerializer,
    CommentReportRetrieveSerializer,
    CommentReportSerializer,
    ImageCommentCreateSerializer,
    ImageCommentListSerializer,
    ImageCommentRetrieveSerializer,
    ImageCommentUpdateSerializer,
    ImageCreateSerializer,
    ImageListSerializer,
    ImageRetrieveSerializer,
    ImageSerializer,
    ImageUpdateSerializer,
    MediaReportCreateSerializer,
    MediaReportListSerializer,
    MediaReportRetrieveSerializer,
    MediaReportSerializer,
    TextCommentCreateSerializer,
    TextCommentListSerializer,
    TextCommentRetrieveSerializer,
    TextCommentUpdateSerializer,
    TextCreateSerializer,
    TextListSerializer,
    TextCommentSerializer,
    ImageCommentSerializer,
    TextRetrieveSerializer,
    TextSerializer,
    TextUpdateSerializer,
    WorldcupCreateSerializer,
    WorldcupListSerializer,
    WorldcupRetrieveSerializer,
    WorldcupSerializer,
    WorldcupUpdateSerializer,
)
from pikuapp.models import (
    CommentReport,
    MediaReport,
    Text,
    Image,
    TextComment,
    ImageComment,
    Worldcup,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import policys


class MediaViewSet(viewsets.ModelViewSet):

    permission_classes = [policys.MediaViewSetPolicy]

    def get_queryset(self):
        MEDIA_MODEL_MANAGERS = {
            "T": Text.objects,
            "I": Image.objects,
        }
        worldcup = (
            Worldcup.objects.filter(pk=self.kwargs["worldcup_pk"])
            .select_related("album")
            .first()
        )
        album = worldcup.album
        media_type = worldcup.media_type
        return MEDIA_MODEL_MANAGERS[media_type].filter(album=album)

    def get_serializer_class(self, *args, **kwargs):
        SERIALIZERS = {
            "list": {
                "T": TextListSerializer,
                "I": ImageListSerializer,
            },
            "create": {
                "T": TextCreateSerializer,
                "I": ImageCreateSerializer,
            },
            "retrieve": {
                "T": TextRetrieveSerializer,
                "I": ImageRetrieveSerializer,
            },
            "update": {
                "T": TextUpdateSerializer,
                "I": ImageUpdateSerializer,
            },
            "partial_update": {
                "T": TextUpdateSerializer,
                "I": ImageUpdateSerializer,
            },
            "delete": {
                "T": TextSerializer,
                "I": ImageSerializer,
            },
        }
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        media_type = worldcup.media_type
        try:
            return SERIALIZERS[self.action][media_type]
        except:
            # FIXME: 더 적절한 처리가 있을 것이라 생각한다.
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MediaReportViewSet(viewsets.ModelViewSet):

    queryset = MediaReport.objects.select_related("worldcup")
    serializer_class = MediaReportSerializer
    permission_classes = [policys.MediaReportViewSetPolicy]

    def get_serializer_class(self):
        QUERYSETS = {
            "list": MediaReportListSerializer,
            "create": MediaReportCreateSerializer,
            "retrieve": MediaReportRetrieveSerializer,
        }
        if queryset := QUERYSETS.get(self.action, None):
            return queryset
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [policys.CommentViewSetPolicy]

    def get_queryset(self):
        COMMENT_MODEL_MANAGERS = {
            "T": TextComment.objects,
            "I": ImageComment.objects,
        }
        worldcup = (
            Worldcup.objects.filter(pk=self.kwargs["worldcup_pk"])
            .select_related("comment_board")
            .first()
        )
        comment_board = worldcup.comment_board
        media_type = worldcup.media_type
        return (
            COMMENT_MODEL_MANAGERS[media_type]
            .filter(comment_board=comment_board)
            .select_related("user", "user__profile", "worldcup")
        )

    def get_serializer_class(self, *args, **kwargs):
        SERIALIZERS = {
            "list": {
                "T": TextCommentListSerializer,
                "I": ImageCommentListSerializer,
            },
            "create": {
                "T": TextCommentCreateSerializer,
                "I": ImageCommentCreateSerializer,
            },
            "retrieve": {
                "T": TextCommentRetrieveSerializer,
                "I": ImageCommentRetrieveSerializer,
            },
            "update": {
                "T": TextCommentUpdateSerializer,
                "I": ImageCommentUpdateSerializer,
            },
            "partial_update": {
                "T": TextCommentUpdateSerializer,
                "I": ImageCommentUpdateSerializer,
            },
            "delete": {
                "T": TextCommentSerializer,
                "I": ImageCommentSerializer,
            },
        }
        worldcup = Worldcup.objects.get(pk=self.kwargs["worldcup_pk"])
        media_type = worldcup.media_type
        try:
            return SERIALIZERS[self.action][media_type]
        except:
            # FIXME: 더 적절한 처리가 있을 것이라 생각한다.
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentReportViewSet(viewsets.ModelViewSet):
    queryset = CommentReport.objects.select_related("worldcup")
    serializer_class = CommentReportSerializer
    permission_classes = [policys.CommentReportViewSetPolicy]

    def get_serializer_class(self):
        print(self.action)
        QUERYSETS = {
            "list": CommentReportListSerializer,
            "create": CommentReportCreateSerializer,
            "retrieve": CommentReportRetrieveSerializer,
        }
        if queryset := QUERYSETS.get(self.action, None):
            return queryset
        return super().get_serializer_class()


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = Worldcup.objects.select_related("album", "creator")
    serializer_class = WorldcupSerializer
    permission_classes = [policys.WorldcupViewSetPolicy]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["media_type"]
    search_fields = ["title", "intro"]
    ordering_fields = ["id", "play_count"]
    ordering = ["-id"]

    def get_serializer_class(self):
        SERIALIZERS = {
            "list": WorldcupListSerializer,
            "create": WorldcupCreateSerializer,
            "retrieve": WorldcupRetrieveSerializer,
            "update": WorldcupUpdateSerializer,
            "partial_update": WorldcupUpdateSerializer,
            "delete": WorldcupSerializer,
        }
        return SERIALIZERS[self.action]