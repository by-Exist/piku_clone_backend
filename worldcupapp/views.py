from rest_framework import viewsets
from . import models
from . import serializers


# TODO: worldcup play count 1 증가시키는 url(post) url 추가
class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = models.Worldcup.objects.select_related("creator__profile").all()
    serializer_class = serializers.WorldCupSerializer


# TODO: media 업로드하는 url(post) 추가
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer