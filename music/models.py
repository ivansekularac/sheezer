from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):
    name = models.CharField(max_length = 100)
    creation_date = models.DateTimeField(auto_now = True)
    songs = models.ManyToManyField('Song')
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Song(models.Model):
    api_id = models.CharField(max_length = 100, primary_key = True)

    def __str__(self):
        return self.api_id
