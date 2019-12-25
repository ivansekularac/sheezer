from django.contrib import admin
from django.urls import path, include
from . import views
from accounts import views as account_views
from music import views as music_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('music/', include('music.urls')),
    path('', views.homepage, name="home"),
]
