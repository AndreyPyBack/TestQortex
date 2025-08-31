from django.core.management.base import BaseCommand
from music.models import Artist, Album, Song, AlbumSong


class Command(BaseCommand):
    help = "Seed initial data: artists, albums, songs with track numbers"

    def handle(self, *args, **options):
        # Artists
        beatles, _ = Artist.objects.get_or_create(name="The Beatles")
        adele, _ = Artist.objects.get_or_create(name="Adele")

        # Albums
        abbey, _ = Album.objects.get_or_create(title="Abbey Road", artist=beatles, release_year=1969)
        twenty1, _ = Album.objects.get_or_create(title="21", artist=adele, release_year=2011)

        # Songs
        come_together, _ = Song.objects.get_or_create(title="Come Together")
        something, _ = Song.objects.get_or_create(title="Something")
        rolling, _ = Song.objects.get_or_create(title="Rolling in the Deep")
        someone, _ = Song.objects.get_or_create(title="Someone Like You")

        # Link songs to albums with track numbers (idempotent)
        AlbumSong.objects.update_or_create(album=abbey, song=come_together, defaults={"track_number": 1})
        AlbumSong.objects.update_or_create(album=abbey, song=something, defaults={"track_number": 2})
        AlbumSong.objects.update_or_create(album=twenty1, song=rolling, defaults={"track_number": 1})
        AlbumSong.objects.update_or_create(album=twenty1, song=someone, defaults={"track_number": 11})

        self.stdout.write(self.style.SUCCESS("Seed data created/updated successfully."))
