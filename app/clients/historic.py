"""
-------------------------------------------------------------------------------------------------
historic
-------------------------------------------------------------------------------------------------
Purpose:
        Update listened song with the last.fm API.

Source:
        https://ws.audioscrobbler.com/2.0/

Input:
        None

Output:
        "MUSIC_TRACK"."HISTORIC": One row inserted for each new song.

Note:
        Track already inserted are skipped.
"""

import requests
import psycopg2

# Information to access last.fm API
API_KEY = "a7955ad0f8a0d65577e476fc67694039"
USER = "LevTakeshy"
url = "https://ws.audioscrobbler.com/2.0/"

params = {
    "method": "user.getrecenttracks",
    "user": USER,
    "api_key": API_KEY,
    "format": "json",
    "limit": 1000
}

response = requests.get(url, params=params)
data = response.json()

tracks = data["recenttracks"]["track"]

conn = psycopg2.connect(
    dbname="music",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Count new listened song
cur.execute("""
    SELECT COUNT(*) 
    FROM "MUSIC_TRACK"."LISTENING_HISTORY"
""")
previous_track = cur.fetchone()
previous_track = previous_track[0]

new_track = 0
for track in tracks:
    song_name = track["name"]
    artist_name = track["artist"]["#text"]
    album_name = track.get("album", {}).get("#text", None)

    listened_at = track.get("date", {}).get("uts")

    album_img_large = track["image"][-1]["#text"] if track.get("image") else None
    new_track = new_track + 1
    cur.execute("""
        INSERT INTO "MUSIC_TRACK"."LISTENING_HISTORY"
        ("SONG_NAME", "ARTIST_NAME", "ALBUM_NAME", "LISTENED_AT", "ALBUM_IMG_LARGE")
        VALUES (%s, %s, %s, to_timestamp(%s), %s)

        ON CONFLICT DO NOTHING
    """, (
        song_name,
        artist_name,
        album_name,
        listened_at,
        album_img_large
    ))

conn.commit()
print(f"New track added: {new_track - previous_track}")
