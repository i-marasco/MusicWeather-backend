import requests
import psycopg2
import time
import os

API_KEY = "a7955ad0f8a0d65577e476fc67694039"
URL = "https://ws.audioscrobbler.com/2.0/"

# DB connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# 1. leggi artisti
cur.execute('SELECT "ARTIST_NAME" FROM "MUSIC_TRACK"."ARTISTS"')
artists = cur.fetchall()


def get_genres(artist_name):
    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }

    r = requests.get(URL, params=params)
    data = r.json()

    # gestione errori API
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

        # IMPORTANT: evita rate limit Last.fm
        time.sleep(0.25)

    except Exception as e:
        print("Error for", artist_name, e)
        conn.rollback()

cur.close()
conn.close()