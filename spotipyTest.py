import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3

from dotenv import load_dotenv

load_dotenv()

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

conn = sqlite3.connect('test1.db')
cursor = conn.cursor()

offset = 0

while True:
    response = sp.playlist_items('spotify:playlist:1vlsJoAKVg4ZIrDNAe2OFa', offset=offset, fields='items.track.id,items.track.name,items.track.artists.name,items.track.album.name,items.track.duration_ms,total', additional_types=['track'])
    
    if len(response['items']) == 0:
        break

    for item in response['items']: 
        cursor.execute('INSERT INTO vtest1 (track_name, track_id, track_duration_ms, artists_names, album_name) values (?, ?, ?, ?, ?)', (item['track']['name'].lower(), item['track']['id'], item['track']['duration_ms'], item['track']['artists'][0]['name'].lower(), item['track']['album']['name'].lower()))
    offset = offset + len(response['items'])
    print(offset, '/', response['total'])

conn.commit()
conn.close()