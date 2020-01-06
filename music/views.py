from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from music.models import Playlist, Song
import requests
import json
import datetime

#  Headers are used in every call and they are always the same
headers = {
    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
    'x-rapidapi-key': "3060c38672msha6ca68fb91aa196p106ce5jsn9c6ba1778834"
}

# Perform Song duration calc
def durationCalc(duration):
    duration = str(datetime.timedelta(seconds = duration))
    return duration[-5:]

# Perform Popularity conversion to float number
def popularityCalc(value):
    return str(round(int(value) / 100000, 1))

# Creating a View for Playlists Page
def playlists_view(request):
    user = request.user
    # We need all playlists created by this user and song counts for which we user annotate func
    playlists = Playlist.objects.filter(created_by = user).annotate(songs_count = Count('songs'))

    # If there is a POST method request we create new playlists
    if 'playlistname' in request.POST:
        playlist_name = request.POST.get('playlistname')
        Playlist.objects.create(name = playlist_name, created_by = user)

    return render(request, 'music/playlists.html', { 'data' : playlists })

# Creating a View for Favorites Page
def favorites_view(request):
    data = []
    # Check if Playlist for My Favorite exists and if not create one
    my_favorites = Playlist.objects.get(name = 'My Favorites', created_by = request.user)
    # Fetch all TrackID's
    songs = my_favorites.songs.all()
    # For each of the ID's we need to make API Call and store that data in list as dict
    for song in songs:
        url = "https://deezerdevs-deezer.p.rapidapi.com/track/" + str(song.api_id)
        response = requests.request("GET", url, headers=headers).json()
        data.append(response)
    # Render Template and pass the data to it
    return render(request, 'music/favorites.html', { 'data': data })

# Creating a View for Browse Page
def explore_view(request):
    return render(request, 'music/explore.html')

# Creating a View for Search Page
def search_view(request):

    data = {}

    if request.method == "GET":
        query = request.GET['search']
        url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        querystring = {"q": query}

        response = requests.request("GET", url, headers = headers, params = querystring).json()
        data.update(response)

        # We need all results since there is 25 per call, we iterate until we got all of them in data dict
        while True:
            if len(response['data']) == 0 or 'next' not in response:
                break

            url_next = response['next']
            response = requests.request("GET", url_next).json()

            for k in response['data']:
                data['data'].append(k)

    # Perform duration and popularity calc for each song
    # for song in data['data']:
    #     song['duration'] = durationCalc(song['duration'])
    #     song['rank'] = popularityCalc(song['rank'])


    # Creating or adding tracks to Playlists
    if request.method == "POST":
        # Creating Playlist by using POST data submitted from modal window
        if 'playlistname' in request.POST:
            user = request.user
            playlist_name = request.POST.get('playlistname')
            Playlist.objects.create(name = playlist_name, created_by = user)
            messages.success(request, 'Playlist has been created successfully!')
        elif 'trackid' in request.POST:
            # If user wants to add a track to existing playlist
            user = request.user
            # Get selected playlist ID
            playlist_id = request.POST.get('playlistid')
            # Find object with that id and save it
            playlist_obj = Playlist.objects.get(id = playlist_id)
            playlist_obj.save()
            # Get track ID and create Song object
            song_id = request.POST.get('trackid')
            song_obj = Song(api_id = song_id)
            song_obj.save()
            # Add Song object to Playlist object
            playlist_obj.songs.add(song_obj)


    # Fetch all User's Playlists for populating Add To feature
    user_playlists = Playlist.objects.filter(created_by = request.user)
    # Pass favorite Songs
    user_favorite_playlist = Playlist.objects.get(name = "My Favorites", created_by = request.user)
    favorite_songs_objs = user_favorite_playlist.songs.all()
    favorite_songs = []
    for song in favorite_songs_objs:
        favorite_songs.append(int(song.api_id))

    # Render template and pass the data we got so it can be used
    return render(request, 'music/search.html', { 'results': data, 'user_playlists': user_playlists, 'favorite_songs': favorite_songs })

# Creating single view track by taking GET param as Track ID
def track_view(request, id):

    url = "https://deezerdevs-deezer.p.rapidapi.com/track/" + str(id)
    response = requests.request("GET", url, headers = headers).json()

    return render(request, 'music/track.html', { 'data': response })

# Creating album view by taking GET param as Album ID
def album_view(request, id):

    url = "https://deezerdevs-deezer.p.rapidapi.com/album/" + str(id)
    response = requests.request("GET", url, headers = headers).json()

    return render(request, 'music/album.html', { 'data': response })

# Creating album view by taking GET param as Album ID
def artist_view(request, id):

    url = "https://deezerdevs-deezer.p.rapidapi.com/artist/" + str(id)
    response = requests.request("GET", url, headers = headers).json()

    return render(request, 'music/artist.html', { 'data': response })

# Creating view for user playlist overview
def playlist_view(request, id):
    # Get Playlist with id passed
    playlist = Playlist.objects.get(id = id)

    # If there is POST request that means we are sending data for removing song from playlist
    if request.method == "POST":
        if 'song_id' in request.POST:
            song_id = request.POST.get('song_id')
            # Use playlist and remove song from it
            song_for_removal = playlist.songs.get(api_id = song_id)
            song_for_removal.delete()

    # Fetch all Songs from that Playlist
    songs = playlist.songs.all()
    # For each of the ID's we need to make API Call and store that data in list as dict
    data = []
    for song in songs:
        url = "https://deezerdevs-deezer.p.rapidapi.com/track/" + str(song.api_id)
        response = requests.request("GET", url, headers = headers).json()
        data.append(response)

    # Perform duration and popularity calc for each song
    for song in data:
        song['duration'] = durationCalc(song['duration'])
        song['rank'] = popularityCalc(song['rank'])

    return render(request, 'music/playlist.html', { 'data': data })


# Creating view for favoriting Songs
def favorited_view(request):
    if request.method == "POST":
        # Check if the song is in favorites already or no, based on that we will remove it or add
        # to favorites on 'heart' button click
        # Save sent id
        song_id = request.POST.get('song_id')
        # Create song object
        #song_obj = Song.objects.create(api_id = song_id)
        # song_obj.save()
        # Add this song to users My Favorite Playlists
        playlist_obj = Playlist.objects.get(name = 'My Favorites', created_by = request.user)
        playlist_obj.save()

        # Check if song is in playlist or no:
        is_favorited = playlist_obj.songs.filter(api_id = song_id)

        if len(is_favorited) > 0:
            # Remove song from playlist because it's already in it
            unvaforited_song = playlist_obj.songs.get(api_id = song_id)
            unvaforited_song.delete()
        else:
            # Add song to this playlists because it's not in it already
            song_obj = Song.objects.create(api_id = song_id)
            song_obj.save()
            playlist_obj.songs.add(song_obj)

    return HttpResponse('Favorited! <3')
