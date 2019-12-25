from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from music.models import Playlist
from django.contrib.auth.models import User



def homepage(request):
    # With this statement we will be 100% that user's first created Playlist will always be My Favorites
    if request.user.is_authenticated:
        favorites = Playlist.objects.filter(name = 'My Favorites', created_by = request.user)
        if len(favorites) == 0:
            my_favorites = Playlist.objects.create(name = 'My Favorites', created_by = request.user)
            my_favorites.save()
    return render(request, 'homepage.html')
