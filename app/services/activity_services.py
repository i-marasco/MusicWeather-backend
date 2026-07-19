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
                    calendar.day::date AS day,
                    COUNT(lh."LISTENED_AT") AS plays
                
                    FROM generate_series(
                        CURRENT_DATE - INTERVAL '1 year',
                        CURRENT_DATE,
                        interval '1 day'
                    ) AS calendar(day)
                
                LEFT JOIN "MUSIC_TRACK"."LISTENING_HISTORY" lh
                    ON DATE(lh."LISTENED_AT") = calendar.day
                
                GROUP BY calendar.day
                
                ORDER BY calendar.day;
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

