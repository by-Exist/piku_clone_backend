from worldcupapp import serializers as worldcup_serializer
from worldcupapp.models import Worldcup
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = Worldcup.objects.select_related("album")
    serializer_class = worldcup_serializer.WorldcupSerializer

    @action(methods=["get"], detail=True)
    def scoreboard(self, request, pk=None):
        worldcup = self.get_object()
        album = worldcup.album
        queryset = self.filter_queryset(album.media_set)
        page = self.paginate_queryset(album.media_set)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        [1, 1, 2, 1, 1] => media 1의 choice_count += 4, media 2의 choice_count += 1"""
        pk_list = request.data["pk_list"]
        MediaModel = self.get_object().album.get_media_model()
        media_qs = MediaModel.objects.filter(pk__in=pk_list)
        for media in media_qs:
            media.choice_count += pk_list.count(media.pk)
        MediaModel.objects.bulk_update(media_qs, ["choice_count"])
        return Response(status=status.HTTP_200_OK)

    def get_serializer_context(self):
        if self.action in ("update", "partial_update", "upload_media"):
            context = super().get_serializer_context()
            album = self.get_object().album
            context.update({"album": album})
            return context
        return super().get_serializer_context()

    def get_serializer_class(self):
        if self.action == "list":
            return worldcup_serializer.WorldcupListSerializer
        elif self.action == "create":
            return worldcup_serializer.WorldcupCreateSerializer
        elif self.action == "retrieve":
            return worldcup_serializer.WorldcupRetrieveSerializer
        elif self.action in ("update", "partial_update"):
            return worldcup_serializer.WorldcupUpdateWithPartialUpdateSerializer
        elif self.action == "scoreboard":
            return worldcup_serializer.MediaScoreboardSerializer
        elif self.action == "upload_media":
            worldcup = self.get_object()
            if worldcup.album.media_type == "T":
                return worldcup_serializer.TextCreateSerializer
            elif worldcup.album.media_type == "I":
                return worldcup_serializer.ImageCreateSerializer
            elif worldcup.album.media_type == "G":
                return worldcup_serializer.GifCreateSerializer
            elif worldcup.album.media_type == "V":
                return worldcup_serializer.VideoCreateSerializer
        elif self.action == "media_win_count_up":
            return worldcup_serializer.MediaWinCountSerializer
        elif self.action == "media_choice_counts_up":
            return worldcup_serializer.MediaChoiceCountsSerializer
        return super().get_serializer_class()