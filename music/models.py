from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_year = models.PositiveIntegerField(null=True, blank=True)

    # Many-to-many through AlbumSong for track ordering
    songs = models.ManyToManyField(Song, through="AlbumSong", related_name="albums")

    class Meta:
        ordering = ["release_year", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.artist})"


class AlbumSong(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["album", "song"], name="unique_song_per_album"),
            models.UniqueConstraint(fields=["album", "track_number"], name="unique_track_number_per_album"),
        ]
        ordering = ["album", "track_number"]

    def __str__(self) -> str:
        return f"{self.album}: {self.track_number}. {self.song}"
