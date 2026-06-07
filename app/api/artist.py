from fastapi import APIRouter, Query
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()
def get_connection():
    return psycopg2.connect(
        dbname="music",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

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

