from worldcupapp import serializers as worldcup_serializer
from worldcupapp.models import Album, Gif, Image, Text, Video, Worldcup
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = Worldcup.objects.all()
    serializer_class = worldcup_serializer.WorldcupSerializer

    @action(methods=["post"], detail=True)
    def upload_media(self, request, pk=None):
        album = self.get_object().album
        MediaModel = album.get_media_model()
        media = MediaModel.objects.create(media=request.data["media"], album=album)
        media.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True)
    def media_win_count_up(self, request, pk=None):
        """media의 pk를 post하면 해당 media의 win_count 필드를 1 증가시킨다."""
        pk = request.data["pk"]
        MediaModel = self.get_object().album.get_media_model()
        media = MediaModel.objects.get(pk=pk)
        media.win_count += 1
        media.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def media_choice_counts_up(self, request, pk=None):
        """media의 pkList를 post하면 해당 media들의 choice_count 필드들을 1 증가시킨다.\n
        [1, 1, 2, 1, 1] => 1번 media의 choice_count += 4, 2번 media의 choice_count += 1"""
        pk_list = request.data["pk_list"]
        MediaModel = self.get_object().album.get_media_model()
        media_qs = MediaModel.objects.filter(pk__in=pk_list)
        for media in media_qs:
            media.choice_count += pk_list.count(media.pk)
        MediaModel.objects.bulk_update(media_qs, ["choice_count"])
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "list":
            return worldcup_serializer.WorldcupListSerializer
        elif self.action == "create":
            return worldcup_serializer.WorldcupCreateSerializer
        elif self.action == "retrieve":
            return worldcup_serializer.WorldcupRetrieveSerializer
        elif self.action == "update":
            return worldcup_serializer.WorldcupUpdateSerializer
        elif self.action == "upload_media":
            return worldcup_serializer.AlbumSerializer.get_media_serializer_class(
                self.get_object().album
            )
        elif self.action == "media_win_count_up":
            return worldcup_serializer.MediaWinCountSerializer
        elif self.action == "media_choice_counts_up":
            return worldcup_serializer.MediaChoiceCountsSerializer
        return super().get_serializer_class()