from accountapp import serializers
from pikuapp.serializers import (
    ImageCommentCreateSerializer,
    ImageCommentListSerializer,
    ImageCreateSerializer,
    ImageListSerializer,
    TextCommentCreateSerializer,
    TextCommentListSerializer,
    TextCreateSerializer,
    TextListSerializer,
    TextSerializer,
    ImageSerializer,
    AlbumSerializer,
    TextCommentSerializer,
    ImageCommentSerializer,
    CommentSerializer,
    WorldcupCreateSerializer,
    WorldcupListSerializer,
    WorldcupPartialUpdateSerializer,
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
    Comment,
    Worldcup,
)
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TextCommentViewSet(viewsets.ModelViewSet):
    queryset = TextComment.objects.all()
    serializer_class = TextCommentSerializer


class ImageCommentViewSet(viewsets.ModelViewSet):
    queryset = ImageComment.objects.all()
    serializer_class = ImageCommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = Worldcup.objects.all()
    serializer_class = WorldcupSerializer

    @action(methods=["get"], detail=True)
    def medias(self, request, pk=None):
        queryset = self.get_object().album.media_set.all()
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)

    @medias.mapping.post
    def upload_media(self, request, pk=None):
        Serializer = self.get_serializer_class()
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            album = self.get_object().album
            serializer.save(album=album)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @action(methods=["get"], detail=True)
    def comments(self, request, pk=None):
        queryset = self.get_object().comment.comment_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @comments.mapping.post
    def upload_comment(self, request, pk=None):
        Serializer = self.get_serializer_class()
        context = self.get_serializer_context()
        serializer = Serializer(data=request.data, context=context)  # context 전달
        if serializer.is_valid():
            comment = self.get_object().comment
            serializer.save(comment=comment)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "upload_comment":
            worldcup = self.get_object()
            context.update(
                {
                    "worldcup": worldcup,
                    "comment": worldcup.comment,
                }
            )
            return context
        return context

    def get_serializer_class(self):
        if self.action == "list":
            return WorldcupListSerializer
        elif self.action == "create":
            return WorldcupCreateSerializer
        elif self.action == "retrieve":
            return WorldcupRetrieveSerializer
        elif self.action == "update":
            return WorldcupUpdateSerializer
        elif self.action == "partial_update":
            return WorldcupPartialUpdateSerializer
        elif self.action == "medias":
            media_type = self.get_object().media_type
            if media_type == "T":
                return TextListSerializer
            elif media_type == "I":
                return ImageListSerializer
        elif self.action == "upload_media":
            media_type = self.get_object().media_type
            if media_type == "T":
                return TextCreateSerializer
            elif media_type == "I":
                return ImageCreateSerializer
        elif self.action == "comments":
            media_type = self.get_object().media_type
            if media_type == "T":
                return TextCommentListSerializer
            elif media_type == "I":
                return ImageCommentListSerializer
        elif self.action == "upload_comment":
            media_type = self.get_object().media_type
            if media_type == "T":
                return TextCommentCreateSerializer
            elif media_type == "I":
                return ImageCommentCreateSerializer
        return super().get_serializer_class()