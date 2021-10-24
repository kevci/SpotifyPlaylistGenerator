import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
import sqlite3
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect('test1.db')
cursor = conn.cursor()

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

parser = argparse.ArgumentParser(description='Generate a Spotify playlist for today')
parser.add_argument('-artists', action='append')
parser.add_argument('-albums', action='append')
parser.add_argument('-tracks', action='append')

args = parser.parse_args()

#tracks, then albums, then artists

for track in args['tracks']:
    
for artist in args['artists']:
    pass



conn.commit()
conn.close()



