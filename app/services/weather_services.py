"""
-------------------------------------------------------------------------------------------------
weather_services.py
-------------------------------------------------------------------------------------------------
Note:
        Called by: api/weather.py
"""
from app.db.conn import get_connection


def get_weather_historic(start_date=None, end_date=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            query = """
                    SELECT
                        "OBSERVED_AT" as observed_at,
                        "CITY" as city,
                        "LAT" as lat,
                        "LON" as lon,
                        "TEMPERATURE" as temperature,
                        "HUMIDITY" as humidity,
                        "PRESSURE" as pressure,
                        "WIND_SPEED" as wind_speed,
                        "WEATHER_CODE" as weather_code
                    FROM "WEATHER"."WEATHER_HISTORY"
                    WHERE 1=1
            """
            params = []

            if start_date:
                query += ' AND "OBSERVED_AT" >= %s'
                params.append(start_date)

            if  end_date:
                query += ' AND "OBSERVED_AT" <= %s'
                params.append(end_date)

            query += ' ORDER BY "OBSERVED_AT" DESC'

            cur.execute(query, params)

            columns = [column[0] for column in cur.description]

            return [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()


def get_weather_daily(start_date = None, end_date = None ):
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            query = """
                SELECT
                    "DAY" as day,
                    "CITY" as city,
                    "LAT" as lat,
                    "LON" as lon,
                    "AVG_TEMPERATURE" as avg_temperature,
                    "MIN_TEMPERATURE" as min_temperature,
                    "MAX_TEMPERATURE" as max_temperature,
                    "AVG_HUMIDITY" as avg_humidity,
                    "AVG_PRESSURE" as avg_pressure,
                    "AVG_WIND_SPEED" as avg_wind_speed,
                    "MOST_COMMON_WEATHER_CODE" as most_common_weather_code
                FROM "WEATHER"."WEATHER_DAILY_SUMMARY"
                WHERE 1=1
            """
            params = []

            if start_date:
                query += ' AND "DAY" >= %s'
                params.append(start_date)

            if end_date:
                query += ' AND "DAY" <= %s'
                params.append(end_date)

            query += ' ORDER BY "DAY" DESC'

            cur.execute(query, params)

            columns = [column[0] for column in cur.description]

            return [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()
