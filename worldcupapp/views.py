from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models
from . import serializers


# TODO: worldcup play count 1 증가시키는 url(post) url 추가
class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = models.Worldcup.objects.select_related("creator__profile", "album")
    serializer_class = serializers.WorldcupSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer

    @action(detail=True, methods=["post"])
    def upload(self, request, pk=None):
        """미디어 업로드 url.\nalbum의 media_type에 따라 적절한 Serializer가 선택된다."""
        album = self.get_object()
        MediaSerializer = serializers.AlbumSerializer.get_media_serializer_class(album)
        print(MediaSerializer)
        print(request.data)
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
            print(serializer)
            return Response(status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "upload":
            album = self.get_object()
            Serializer = serializers.AlbumSerializer.get_media_serializer_class(album)
            return Serializer
        return super().get_serializer_class()