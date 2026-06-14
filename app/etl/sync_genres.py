"""
-------------------------------------------------------------------------------------------------
sync_genres.py
-------------------------------------------------------------------------------------------------
Purpose:
        Update the list of listened genres.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"

Input:
        None

Output:
        "MUSIC_TRACK"."GENRES" : One row inserted for each new genres listened.

Note:
       The line inserted is a list: {rock,"hard rock","classic rock",80s,"hair metal"}.
       In last.fm doesn't exist a way for have the genres of a song, the genres is based on the singer.
"""

import requests
import time
import os
from app.db.conn import get_connection
from dotenv import load_dotenv

load_dotenv()

LASTFM_URL = os.getenv("LASTFM_URL")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
           SELECT "ARTIST_NAME" FROM "MUSIC_TRACK"."ARTISTS" 
           """)
artists = cur.fetchall()


def get_genres(artist_name):
    """
    :param
        artist_name: Name of the artist.
    :return:
        List of genres associated with every artist.
    """
    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    r = requests.get(LASTFM_URL, params=params)
    data = r.json()

    # Manage if an artis is not associated to a genres.
    if "toptags" not in data or "tag" not in data["toptags"]:
        return []

    tags = data["toptags"]["tag"]
    return [t["name"] for t in tags[:5]]


for artist_name in artists:
    try:
        genres = get_genres(artist_name)
        print(artist_name, genres)

        main_genre = genres[0] if genres else None

        cur.execute(
            """
            INSERT INTO "MUSIC_TRACK"."GENRES"
            ("ARTIST_NAME", "GENRE_LIST", "MAIN_GENRE")
            VALUES (%s, %s, %s)
            ON CONFLICT ("ARTIST_NAME")
            DO UPDATE SET
                "GENRE_LIST" = EXCLUDED."GENRE_LIST",
                "MAIN_GENRE" = EXCLUDED."MAIN_GENRE"
            """,
            (artist_name, genres, main_genre)
        )

        conn.commit()

        # IMPORTANT: avoid last.fm rate limit.
        time.sleep(0.25)

    except Exception as e:
        print("Error for", artist_name, e)
        conn.rollback()

cur.close()
conn.close()
