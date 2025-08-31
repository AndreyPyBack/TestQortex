from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Artist, Album, Song
from .serializers import (
    ArtistListSerializer,
    ArtistDetailSerializer,
    AlbumListSerializer,
    AlbumDetailSerializer,
    AlbumWriteSerializer,
    SongSerializer,
)


# Create your views here.

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by("name")
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ["list", "create", "update", "partial_update"]:
            return ArtistListSerializer
        return ArtistDetailSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.select_related("artist").all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ["list", "create", "update", "partial_update"]:
            return AlbumWriteSerializer if self.action != "list" else AlbumListSerializer
        return AlbumDetailSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]
