import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from music.models import Playlist, Song, Explore, Deezer

# Creating a View for Playlists Page
def playlists_view(request):
    # We need all playlists created by this user and song counts
    playlists = Playlist.fetch_playlists(request.user)

    # If there is a POST method request we create new playlists
    if 'playlistname' in request.POST:
        Playlist.create_playlist(request.POST.get('playlistname'), request.user)
        messages.info(request, 'Playlist has been created successfully!')

    return render(request, 'music/playlists.html', { 'data' : playlists })

# Creating a View for Favorites Page
def favorites_view(request):
    # Check if Playlist for My Favorite exists and if not create one
    my_favorites = Playlist.objects.get(name='My Favorites', created_by=request.user)
    # Fetch all TrackID's
    songs = my_favorites.songs.all()
    # For each of the ID's we need to make API Call and store that data in list as dict
    s = Deezer.multi_calls(songs)

    # # If there is POST request that means we are sending data for removing song from playlist
    # if request.method == "POST":
    #     if 'song_id' in request.POST:
    #         Song.remove_from_playlist(my_favorites.id, request.POST.get('song_id'))

    # Render Template and pass the data to it
    return render(request, 'music/favorites.html', { 'data': s })

# Creating a View for Browse Page
def explore_view(request):
    # Select only playlist excluding My Favorites ordered by date of creation
    last_four = Explore.newest_playlists()
    # Fetch most popular songs by users based on in how many playlist song has been added
    most_popular = Explore.popular_songs()
    # For each of the songs we need to make api call and return the data 
    popular_data = Deezer.multi_calls(most_popular)

    return render(request, 'music/explore.html', { 'data': last_four, 'most_popular': popular_data })
    
# Creating a View for Top Deezer Playlists
def top_view(request, id):
    
    response = Deezer.call('https://deezerdevs-deezer.p.rapidapi.com/playlist/', id=id)
    return render(request, 'music/top.html', { 'data': response })


# Creating a View for Search Page
def search_view(request):

    data = {}

    if request.method == "GET":
        querystring = {"q": request.GET['search']}
        response = Deezer.call('https://deezerdevs-deezer.p.rapidapi.com/search', query=querystring)
        data.update(response)

        # We need all results since there is 25 per call, we iterate until we got all of them in data dict
        while True:
            if len(response['data']) == 0 or 'next' not in response:
                break

            url_next = response['next']
            response = requests.request("GET", url_next).json()

            for k in response['data']:
                data['data'].append(k)

    # Creating or adding tracks to Playlists
    if request.method == "POST":
        # Creating Playlist by using POST data submitted from modal window
        if 'playlistname' in request.POST:
            Playlist.create_playlist(request.POST.get('playlistname'), request.user)            
            messages.success(request, 'Playlist has been created successfully!')
        elif 'trackid' in request.POST:            
            # Get selected playlist ID and Song ID
            playlist = request.POST.get('playlistid')
            song = request.POST.get('trackid')
            # Call method from models.Song for adding song to playlist
            Song.add_to_playlist(playlist, song)

    # Fetch all User's Playlists for populating Add To feature
    user_playlists = Playlist.objects.filter(created_by=request.user)
    # Pass favorite Songs
    favorite_songs = Song.fetch_favorites(request.user)

    # Render template and pass the data we got so it can be used
    return render(request, 'music/search.html', { 'results': data, 'user_playlists': user_playlists, 'favorite_songs': favorite_songs })

# Creating single view track by taking GET param as Track ID
def track_view(request, id):

    response = Deezer.call('https://deezerdevs-deezer.p.rapidapi.com/track/', id=id)
    return render(request, 'music/track.html', { 'data': response })

# Creating album view by taking GET param as Album ID
def album_view(request, id):

    response = Deezer.call('https://deezerdevs-deezer.p.rapidapi.com/album/', id=id)
    
    # Pass favorite Songs
    favorite_songs = Song.fetch_favorites(request.user)

    return render(request, 'music/album.html', { 'data': response, 'favorite_songs': favorite_songs })

# Creating album view by taking GET param as Album ID
def artist_view(request, id):
    
    # Make API Call for particular artist ID
    response = Deezer.call('https://deezerdevs-deezer.p.rapidapi.com/artist/', id=id)
    # Make a call after for top 20 tracks for that Artist ID
    top20_response = Deezer.call('https://api.deezer.com/artist/', id=id, endstring='/top?limit=20')
    # Save all to dict for passing the data to the template
    context = {
        'artist': response,
        'top20': top20_response
    }
    
    # Pass favorite Songs
    favorite_songs = Song.fetch_favorites(request.user)    
    return render(request, 'music/artist.html', { 'data': context, 'favorite_songs': favorite_songs })

# Creating view for user playlist overview
def playlist_view(request, id):

    # If there is POST request that means we are sending data for removing song from playlist
    if request.method == "POST":
        if 'song_id' in request.POST:
            Song.remove_from_playlist(id, request.POST.get('song_id'))
        # if there is delete in POST we delete that playlist and redirect to homepage with success message
        elif 'delete' in request.POST:
            Playlist.delete_playlist(id)
            messages.info(request, 'Playlist has been deleted successfully!')
            return redirect('music:playlists')

    playlist = Playlist.objects.get(id=id)
    # Fetch all Songs from that Playlist
    songs = Playlist.fetch_songs(id)
    # Call multi calls api for each of the songs
    data = Deezer.multi_calls(songs)

    return render(request, 'music/playlist.html', { 'data': data, 'playlist': playlist })

# Creating view for favoriting Songs
def favorited_view(request):
    if request.method == "POST":        
        # This one is called on Heart icon clicked
        # Call staticmethod from Song class
        Song.favorite(request.user, request.POST.get('song_id'))

    return HttpResponse('Favorited! <3')
