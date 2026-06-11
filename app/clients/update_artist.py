"""
-------------------------------------------------------------------------------------------------
update_artist
-------------------------------------------------------------------------------------------------
Purpose:
        Update the list of listened artist based on listening history.

Source:
        "MUSIC_TRACK"."HISTORIC"

Input:
        None

Output:
        "MUSIC_TRACK"."ARTISTS": One row inserted for each new artist listened.

Note:
        Stores the total track listened per artist.
"""

import requests
import psycopg2

API_KEY = "a7955ad0f8a0d65577e476fc67694039"
USER = "LevTakeshy"
url = "https://ws.audioscrobbler.com/2.0/"

conn = psycopg2.connect(
    dbname="music",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
            INSERT INTO "MUSIC_TRACK"."ARTISTS" (
                "ARTIST_NAME",
                "PLAYS",
                "LISTENED_AT"
            )
            SELECT
                "ARTIST_NAME",
                COUNT(*) AS plays,
                MIN("LISTENED_AT") AS first_listened_at
            FROM "MUSIC_TRACK"."LISTENING_HISTORY"
            GROUP BY "ARTIST_NAME"
        
            ON CONFLICT ("ARTIST_NAME")
            DO UPDATE SET
                "PLAYS" = EXCLUDED."PLAYS",
                "LISTENED_AT" = EXCLUDED."LISTENED_AT";
""")

conn.commit()

conn.commit()
print(f"Artist updated")
