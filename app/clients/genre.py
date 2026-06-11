"""
-------------------------------------------------------------------------------------------------
genre
-------------------------------------------------------------------------------------------------
Purpose:
        Update the list of listened genres.

Source:
        "MUSIC_TRACK"."HISTORIC".

Input:
        None

Output:
        "MUSIC_TRACK"."GENRES" : One row inserted for each new genres listened.

Note:
       The line inserted is a list: {rock,"hard rock","classic rock",80s,"hair metal"}.
       In last.fm doesn't exist a way for have the genres of a song, the genres is based on the singer.
"""

import requests
import psycopg2
import time

API_KEY = "a7955ad0f8a0d65577e476fc67694039"
URL = "https://ws.audioscrobbler.com/2.0/"

conn = psycopg2.connect(
    dbname="music",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
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
        "api_key": API_KEY,
        "format": "json"
    }

    r = requests.get(URL, params=params)
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

        cur.execute(
            """
            INSERT INTO "MUSIC_TRACK"."GENRES" ("ARTIST_NAME", "GENRE_LIST")
            VALUES (%s, %s)
            ON CONFLICT ("ARTIST_NAME") DO NOTHING;
            """,
            (artist_name, genres)
        )

        conn.commit()

        # IMPORTANT: avoid last.fm rate limit.
        time.sleep(0.25)

    except Exception as e:
        print("Error for", artist_name, e)
        conn.rollback()

cur.close()
conn.close()
