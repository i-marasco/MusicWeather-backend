"""
-------------------------------------------------------------------------------------------------
genre_ranking_services.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/genre_ranking.py
"""

from fastapi import APIRouter
from app.db.conn import get_connection

router = APIRouter()

def generate_ranking(period: str, start_date, end_date):
    print("GENRE RANKING STARTED")
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                    INSERT INTO "MUSIC_TRACK"."GENRE_RANKINGS" (
                        "PERIOD_TYPE",
                        "PERIOD_START",
                        "PERIOD_END",
                        "GENRE",
                        "RANK_POSITION",
                        "PLAYS"
                    )
                    SELECT
                        %s,
                        %s,
                        %s,
                        t.genre,
                        RANK() OVER (ORDER BY t.plays DESC),
                        t.plays
                    FROM (
                        SELECT
                            g."MAIN_GENRE" AS genre,
                            COUNT(*) AS plays
                        FROM "MUSIC_TRACK"."LISTENING_HISTORY" lh
                        JOIN "MUSIC_TRACK"."GENRES" g
                            ON lh."ARTIST_NAME" = g."ARTIST_NAME"
                        WHERE g."MAIN_GENRE" IS NOT NULL
                          AND lh."LISTENED_AT" >= %s
                          AND lh."LISTENED_AT" < %s
                        GROUP BY g."MAIN_GENRE"
                    ) t
                    ON CONFLICT ("PERIOD_TYPE", "PERIOD_START", "GENRE")
                    DO UPDATE SET
                        "RANK_POSITION" = EXCLUDED."RANK_POSITION",
                        "PLAYS" = EXCLUDED."PLAYS";
            """, (period, start_date, end_date, start_date, end_date))

            conn.commit()

    finally:
        conn.close()
