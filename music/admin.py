from django.contrib import admin

from .models import Artist, Album, Song, AlbumSong


class AlbumSongInline(admin.TabularInline):
    model = AlbumSong
    extra = 1
    fields = ("song", "track_number")
    ordering = ("track_number",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "release_year")
    list_filter = ("artist", "release_year")
    search_fields = ("title", "artist__name")
    inlines = [AlbumSongInline]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)
