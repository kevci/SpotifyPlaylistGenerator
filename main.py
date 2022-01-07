import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
import sqlite3
import os
import random
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect('test1.db')
cur = conn.cursor()

scope = 'playlist-read-private, playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

parser = argparse.ArgumentParser(description='Generate a Spotify playlist for today')
parser.add_argument('-artists', action='append')
parser.add_argument('-albums', action='append')
parser.add_argument('-tracks', action='append')
parser.add_argument('-limit')

args = parser.parse_args()

#tracks, then albums, then artists
selectedTrackIds = set()

if args.limit:
    num_total = int(args.limit)
else:
    num_total = int(os.getenv('DEFAULT_TRACK_LIMIT'))
    
if args.tracks:
    num_by_track = num_total - len(args.tracks)
else:
    num_by_track = 0

if args.artists:
    num_for_each_artist = (num_total - num_by_track) // len(args.artists)

if args.tracks:
    for i, track in enumerate(args.tracks):
        cur.execute('select track_id from vtest1 where track_name match (:track_name) order by rank limit 1', {'track_name': args.tracks[i]})
        selectedTrackIds.add(cur.fetchone()[0])
    
if args.artists:
    for i, artist in enumerate(args.artists):
        if len(selectedTrackIds):
            joinedTrackIds = ' '.join(selectedTrackIds)
        else:
            joinedTrackIds = ''
        cur.execute('select track_id from vtest1 where artists_names match (:artists_names) and track_id not in (:selected_track_ids) order by random(), rank limit :num_for_each_artist', {'artists_names': args.artists[i], 'selected_track_ids': joinedTrackIds, 'num_for_each_artist': str(num_for_each_artist)})
        #cur.execute(f'''select track_id from vtest1 where artists_names match '{args.artists[i]}' and track_id not in ({' '.join(selectedTrackIds)}) order by rank limit {num_for_each_artist}''')
        #cur.execute(f'select track_id from vtest1 where track_id not in ({joinedTrackIds}) limit {num_for_each_artist}')
        results = cur.fetchall()
        for result in results:
            selectedTrackIds.add(result[0])

left_over = num_total - len(selectedTrackIds)

for _ in range(left_over):
    if len(selectedTrackIds):
        joinedTrackIds = ' '.join(selectedTrackIds)
    else:
        joinedTrackIds = ''
    cur.execute('select track_id from vtest1 where track_id not in (:selected_track_ids) order by random() limit 1', {'selected_track_ids': joinedTrackIds})
    selectedTrackIds.add(cur.fetchone()[0])

randomizedSelectedTrackIds = random.sample(selectedTrackIds, len(selectedTrackIds))

for track in randomizedSelectedTrackIds:
    sp.playlist_replace_items(os.getenv('DEFAULT_PLAYLIST_ID'), randomizedSelectedTrackIds)

conn.commit()
conn.close()



