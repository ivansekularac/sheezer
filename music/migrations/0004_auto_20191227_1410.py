# Generated by Django 3.0.1 on 2019-12-27 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_playlist_song'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='playlists',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
    ]
