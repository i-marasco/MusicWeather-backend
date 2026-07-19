"""
-------------------------------------------------------------------------------------------------
activity_services.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/activity.py
"""

from app.db.conn import get_connection


def get_calendar(
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    DATE("LISTENED_AT") AS day,
                    COUNT(*) AS plays
                FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                GROUP BY DATE("LISTENED_AT")
                ORDER BY day;
            """)

            rows = cur.fetchall()

            columns = [column[0] for column in cur.description]

            calendar = [
                dict(zip(columns, row))
                for row in rows
            ]

            return {
                "calendar": calendar
            }

    finally:
        conn.close()

