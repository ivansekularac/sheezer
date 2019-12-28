from django.urls import path, include
from . import views

app_name = 'music'

urlpatterns = [
    path('playlists/', views.playlists_view, name="playlists"),
    path('playlists/<int:id>/', views.playlist_view, name="playlist"),
    path('favorites/', views.favorites_view, name="favorites"),
    path('browse/', views.browse_view, name="browse"),
    path('search', views.search_view, name="search"),
    path('track/<int:id>/', views.track_view, name="track"),
    path('track/favorited', views.favorited_view, name="favorited"),
    path('album/<int:id>/', views.album_view, name="album"),
    path('artist/<int:id>/', views.artist_view, name="artist"),
]
