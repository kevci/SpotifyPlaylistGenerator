import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

conn = sqlite3.connect('localTracks.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE tracks (name TEXT, uri TEXT, duration_ms INTEGER, artists TEXT, album TEXT)')

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))