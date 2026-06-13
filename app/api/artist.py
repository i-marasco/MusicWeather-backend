"""
-------------------------------------------------------------------------------------------------
artist
-------------------------------------------------------------------------------------------------
Purpose:
        Output all the artist listened.

Source:
        "MUSIC_TRACK"."ARTISTS"

Input:
        None

Output:
        /artist:
        Artist name and first time listened.
"""

from fastapi import APIRouter
from app.database.conn import get_connection

router = APIRouter()
conn = get_connection()
cur = conn.cursor()

@router.get("/artist")
def get_artist(
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT "ARTIST_NAME", "LISTENED_AT", "PLAYS"
                    FROM "MUSIC_TRACK"."ARTISTS"
            """)

            rows = cur.fetchall()

    finally:
        conn.close()

    return {
        "artists": rows
    }

