"""
-------------------------------------------------------------------------------------------------
artist_services.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/artist.py
"""

from app.db.conn import get_connection


def get_artist(
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT "ARTIST_NAME" as artist_name,
                           "LISTENED_AT" as listened_at,
                            "PLAYS" as plays
                    FROM "MUSIC_TRACK"."ARTISTS"
                    ORDER BY plays DESC
            """)

            rows = cur.fetchall()

            columns = [column[0] for column in cur.description]

            artists = [
                dict(zip(columns, row))
                for row in rows
            ]

            return {
                "artists": artists
            }

    finally:
        conn.close()

