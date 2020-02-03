from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
import datetime

# Model for Playlists created by Users
# Each of the playlists created has creation date, many to many field songs and who created it
class Playlist(models.Model):
    name = models.CharField(max_length = 100)
    creation_date = models.DateTimeField(auto_now = True)
    songs = models.ManyToManyField('Song')
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

   
    @staticmethod
    def create_playlist(playlist_name, user):
        """Simple method for creating new Playlist in Database"""
        Playlist.objects.create(name=playlist_name, created_by=user)

    @staticmethod
    def delete_playlist(playlist_id):
        """Simple method for deleting Playlist object from database"""
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()

    @staticmethod
    def fetch_songs(playlist_id):
        """Simple method for fetching all songs from playlist"""
        playlist = Playlist.objects.get(id=playlist_id)
        return playlist.songs.all()


    @staticmethod
    def fetch_playlists(user):
        """Simple method for returning all playlists created by user including count of songs per playlist"""
        # We need all playlists created by this user and song counts for which we user annotate func
        return Playlist.objects.filter(created_by=user).annotate(songs_count=Count('songs'))



# Model for Songs, since we don't have database with song information
# we need to store api_id for particualar song so we can perform some actions later
# it's primary key since we don't want multiple rows for same songs

class Song(models.Model):
    api_id = models.CharField(max_length = 100, primary_key = True)

    def __str__(self):
        return self.api_id

    @staticmethod
    def favorite(user, song_id):
        """This static method handles adding song to users My Favorites playlist
        and removes it if it's already added"""
        # Add this song to users My Favorite Playlists
        playlist = Playlist.objects.get(name='My Favorites', created_by=user)
        playlist.save()
        # Filter song objects for that list.. This returns a list
        results = playlist.songs.filter(api_id=song_id)

        if len(results) > 0:
            # Remove song from playlist because it's already in it
            song = playlist.songs.get(api_id=song_id)
            song.delete()
        else:
            # Add song to this playlists because it's not in it already
            # First see if the song is already in db
            song_results = Song.objects.filter(api_id=song_id)
            if len(song_results) == 0:
                song = Song.objects.create(api_id=song_id)
                song.save()
            else:
                song = Song.objects.get(api_id=song_id)
                
            playlist.songs.add(song)

    @staticmethod
    def fetch_favorites(user):
        """This static method is returning all favorited songs by user"""
        # Get My Favorites playlist
        favorites_playlist = Playlist.objects.get(name='My Favorites', created_by=user)
        # Fetch all Song objects from it
        favorite_songs_objs = favorites_playlist.songs.all()
        # Make a list where we will append only api_id which we need
        favorite_songs = []
        for song in favorite_songs_objs:
            favorite_songs.append(int(song.api_id))

        return favorite_songs


    @staticmethod
    def add_to_playlist(playlist_id, song_id):
        """This static method is adding song to existing playlist"""
        # Find object with that id and save it
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.save()
        # Get track ID and create Song object
        song = Song(api_id = song_id)
        song.save()
        # Add Song object to Playlist object
        playlist.songs.add(song)

    @staticmethod
    def remove_from_playlist(playlist_id, song_id):
        """This static method removes song from playlist"""
        # Get Playlist object from database
        playlist = Playlist.objects.get(id=playlist_id)
        # Get song from playlist and delete it
        song = playlist.songs.get(api_id=song_id)
        song.delete()


class Explore:

    @staticmethod
    def newest_playlists():
        """This static method returns last 4 created playlists created by users"""
        # Select only playlist excluding My Favorites ordered by date of creation
        return Playlist.objects.order_by('-creation_date').exclude(name='My Favorites')[:4]

    @staticmethod
    def popular_songs():
        """This static method returns 6 most added songs to playlists by users"""
        # Fetch most popular songs by users based on in how many playlist song has been added
        return Song.objects.all().annotate(count=Count('playlist')).order_by('-count')[:6]

    