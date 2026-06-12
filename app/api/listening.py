"""
-------------------------------------------------------------------------------------------------
listening
-------------------------------------------------------------------------------------------------
Purpose:
        Output the song listened in a period or historic.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"

Input:
        start_date(optional):  start date of the selection period.
        end_date(optional): end date of the selection period.

Output:
        /history:
            Return the song listened in a period or historic.
        /period:
            Return the period of listening M: Morning, A: Afternoon, E: Evening, N: Night.
"""

from fastapi import APIRouter, Query
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from app.database.conn import get_connection

router = APIRouter()
conn = get_connection()
cur = conn.cursor()

@router.get("/history")
def get_history(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    """
    :param
        start_date: start date
        end_date: end date
    :return
        List of the artist listened in the selected period.
    """
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            query = """
                SELECT "SONG_NAME", "ARTIST_NAME", "LISTENED_AT"
                FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                WHERE 1=1
            """

            params = []

            # Add filters only if provided
            if start_date is not None:
                query += ' AND "LISTENED_AT" >= %s'
                params.append(start_date)

            if end_date is not None:
                query += ' AND "LISTENED_AT" <= %s'
                params.append(end_date)

            query += ' ORDER BY "LISTENED_AT" ASC'

            cur.execute(query, params)
            rows = cur.fetchall()

    finally:
        conn.close()

    tracks = [
        {
            "track": r[0],
            "artist": r[1],
            "listened_at": r[2].isoformat()
        }
        for r in rows
    ]

    return {
        "total_plays": len(tracks),
        "tracks": tracks
    }

@router.get("/period")
def get_period(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    """
    :param
        start_date: start date
        end_date: end date
    :return
        Return the period of listening M: Morning, A: Afternoon, E: Evening, N: Night.
    """
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            query = """
                        SELECT
                            period,
                            plays,
                            ROUND(
                                plays * 100.0 / SUM(plays) OVER (),
                                2
                            ) AS percentage
                        FROM (
                            SELECT
                                CASE
                                    WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 6
                                         AND EXTRACT(HOUR FROM "LISTENED_AT") < 12 THEN 'Morning'
                                    WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 12
                                         AND EXTRACT(HOUR FROM "LISTENED_AT") < 18 THEN 'Afternoon'
                                    WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 18
                                         AND EXTRACT(HOUR FROM "LISTENED_AT") < 21 THEN 'Evening'
                                    ELSE 'Night'
                                END AS period,
                                COUNT(*) AS plays
                            FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                            WHERE 1=1
            """

            params = []

            if start_date is not None:
                query += ' AND "LISTENED_AT" >= %s'
                params.append(start_date)

            if end_date is not None:
                query += ' AND "LISTENED_AT" <= %s'
                params.append(end_date)

            query += """
                GROUP BY
                    CASE
                        WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 6
                             AND EXTRACT(HOUR FROM "LISTENED_AT") < 12 THEN 'Morning'
                        WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 12
                             AND EXTRACT(HOUR FROM "LISTENED_AT") < 18 THEN 'Afternoon'
                        WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 18
                             AND EXTRACT(HOUR FROM "LISTENED_AT") < 21 THEN 'Evening'
                        ELSE 'Night'
                    END
            ) t
            ORDER BY period;
            """

            cur.execute(query, params)
            results = cur.fetchall()

    finally:
        conn.close()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "data": results
    }