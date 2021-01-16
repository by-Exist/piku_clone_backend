from pikuapp.serializers import (
    TextSerializer,
    ImageSerializer,
    AlbumSerializer,
    TextCommentSerializer,
    ImageCommentSerializer,
    CommentSerializer,
    WorldcupSerializer,
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
from rest_framework import viewsets


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