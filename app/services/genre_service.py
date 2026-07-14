"""
-------------------------------------------------------------------------------------------------
genres_service.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/genres.py
"""

from app.db.conn import get_connection

def get_top_genres(start_date=None, end_date=None):
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            query = """
                    SELECT
                        g."MAIN_GENRE" AS genre,
                        COUNT(*) AS plays
                    FROM "MUSIC_TRACK"."LISTENING_HISTORY" lh
                    JOIN "MUSIC_TRACK"."GENRES" g
                        ON lh."ARTIST_NAME" = g."ARTIST_NAME"
                    WHERE g."MAIN_GENRE" IS NOT NULL
            """

            params = []

            # add date filter only if provided
            if start_date and end_date:
                query += """
                    AND "LISTENED_AT" BETWEEN %s AND %s
                """
                params.extend([start_date, end_date])

            query += """
                GROUP BY "MAIN_GENRE"
                ORDER BY plays DESC;
            """

            cur.execute(query, params)
            rows = cur.fetchall()

            return [
                {
                    "genre": r[0],
                    "plays": r[1]
                }
                for r in rows
            ]

    finally:
        conn.close()


def get_genres_by_period(start_date = None, end_date = None):
        """
        :param
            start_date: start date
            end_date: end date
        :return

        """
        conn = get_connection()

        try:
            with conn.cursor() as cur:

                query = """
                    SELECT
                        CASE
                            WHEN EXTRACT(HOUR FROM lh."LISTENED_AT") >= 6
                             AND EXTRACT(HOUR FROM lh."LISTENED_AT") < 12 THEN 'Morning'
                            WHEN EXTRACT(HOUR FROM lh."LISTENED_AT") >= 12
                             AND EXTRACT(HOUR FROM lh."LISTENED_AT") < 18 THEN 'Afternoon'
                            WHEN EXTRACT(HOUR FROM lh."LISTENED_AT") >= 18
                             AND EXTRACT(HOUR FROM lh."LISTENED_AT") < 21 THEN 'Evening'
                            ELSE 'Night'
                        END AS period,
                        g."MAIN_GENRE" AS genre,
                        COUNT(*) AS plays
                    FROM "MUSIC_TRACK"."LISTENING_HISTORY" lh
                    JOIN "MUSIC_TRACK"."GENRES" g
                        ON lh."ARTIST_NAME" = g."ARTIST_NAME"
                    WHERE g."MAIN_GENRE" IS NOT NULL
                        """

                params = []

                if start_date is not None:
                    query += ' AND "LISTENED_AT" >= %s'
                    params.append(start_date)

                if end_date is not None:
                    query += ' AND "LISTENED_AT" <= %s'
                    params.append(end_date)

                query += """
                    GROUP BY period, g."MAIN_GENRE"
                    ORDER BY period, plays DESC
                """

                cur.execute(query, params)
                rows = cur.fetchall()

                columns = [column[0] for column in cur.description]

                genres = [
                    dict(zip(columns, row))
                    for row in rows
                ]

        finally:
            conn.close()

        return {
            "start_date": start_date,
            "end_date": end_date,
            "data": genres
        }