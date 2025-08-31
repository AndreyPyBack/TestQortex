from rest_framework import serializers
from .models import Artist, Album, Song, AlbumSong


class SongInlineInAlbumSerializer(serializers.ModelSerializer):
    track_number = serializers.IntegerField()

    class Meta:
        model = Song
        fields = ("id", "title", "track_number")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # track_number from through model
        if hasattr(instance, 'albumsong'):
            data['track_number'] = instance.albumsong.track_number
        elif instance.through_fields:
            pass
        return data


class AlbumListSerializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ("id", "title", "artist", "release_year")


class AlbumDetailSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()
    artist = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ("id", "title", "artist", "release_year", "songs")

    def get_songs(self, album: Album):
        qs = Song.objects.filter(albums=album).order_by("albumsong__track_number").distinct()
        # annotate track numbers via through relation access in serializer
        for s in qs:
            s.albumsong = AlbumSong.objects.get(album=album, song=s)
        return SongInlineInAlbumSerializer(qs, many=True).data


class AlbumWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("id", "title", "artist", "release_year")


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("id", "title")


class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name")


class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("id", "name", "albums")

    def get_albums(self, artist: Artist):
        albums = Album.objects.filter(artist=artist).order_by("release_year", "title")
        return AlbumDetailSerializer(albums, many=True).data
