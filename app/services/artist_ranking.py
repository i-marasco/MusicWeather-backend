"""
-------------------------------------------------------------------------------------------------
artist_ranking
-------------------------------------------------------------------------------------------------
Purpose:
        Rank the artist WEEKLY or MONTHLY for number of track listened.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"

Input:
        None

Output:
        "MUSIC_TRACK"."ARTIST_RANKINGS":
        WEEKLY: Add one row for every artist listened in the current week.
        MONTHLY: Add one row for every artist listened in the current month.
"""

from fastapi import APIRouter
from app.database.conn import get_connection

router = APIRouter()

conn = get_connection()
cur = conn.cursor()

def generate_ranking(period: str, start_date, end_date):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "MUSIC_TRACK"."ARTIST_RANKINGS" (
                    "PERIOD_TYPE",
                    "PERIOD_START",
                    "PERIOD_END",
                    "ARTIST_NAME",
                    "RANK_POSITION",
                    "PLAYS"
                )
                SELECT
                    %s,
                    %s,
                    %s,
                    t."ARTIST_NAME",
                    RANK() OVER (ORDER BY t.plays DESC),
                    t.plays
                FROM (
                    SELECT
                        "ARTIST_NAME",
                        COUNT(*) AS plays
                    FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                    WHERE DATE("LISTENED_AT") >= %s
                      AND DATE("LISTENED_AT") < %s
                    GROUP BY "ARTIST_NAME"
                ) t
                ON CONFLICT ("PERIOD_TYPE", "PERIOD_START", "ARTIST_NAME")
                DO UPDATE SET
                    "RANK_POSITION" = EXCLUDED."RANK_POSITION",
                    "PLAYS" = EXCLUDED."PLAYS";
            """, (period, start_date, end_date, start_date, end_date))

            conn.commit()

    finally:
        conn.close()
