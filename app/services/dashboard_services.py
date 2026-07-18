"""
-------------------------------------------------------------------------------------------------
dashboard.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/dashboard.py
"""

from app.db.conn import get_connection


def get_dashboard(
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM "MUSIC_TRACK"."ARTISTS"
            """)

            artists = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM "MUSIC_TRACK"."LISTENING_HISTORY"
            """)

            tracks = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(DISTINCT "MAIN_GENRE")
                FROM "MUSIC_TRACK"."GENRES"
                WHERE "MAIN_GENRE" IS NOT NULL
            """)

            genres = cur.fetchone()[0]

            cur.execute("""
                SELECT
                    "ARTIST_NAME" AS artist_name,
                    "PLAYS" AS plays
                FROM "MUSIC_TRACK"."ARTISTS"
                ORDER BY "PLAYS" DESC
                LIMIT 1
            """)

            row = cur.fetchone()

            top_artist = {
                "artist_name": row[0],
                "plays": row[1]
            }

            cur.execute("""
                SELECT
                    "TEMPERATURE" AS temperature,
                    "CITY" AS city
                FROM "WEATHER"."WEATHER_HISTORY"
                ORDER BY "OBSERVED_AT" DESC
                LIMIT 1
            """)

            row = cur.fetchone()

            latest_weather = {
                "temperature": row[0],
                "city": row[1]
            }

            return {
                "artists": artists,
                "tracks": tracks,
                "genres": genres,
                "top_artist": top_artist,
                "latest_weather": latest_weather,
            }

    finally:
        conn.close()

