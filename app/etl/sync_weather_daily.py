from app.db.conn import get_connection


def sync_weather_daily():
        conn = get_connection()

        try:
            with conn.cursor() as cur:

                    cur.execute("""
                                INSERT INTO "WEATHER"."WEATHER_DAILY_SUMMARY" ("DAY",
                                                                               "CITY",
                                                                               "LAT",
                                                                               "LON",
                                                                               "AVG_TEMPERATURE",
                                                                               "MIN_TEMPERATURE",
                                                                               "MAX_TEMPERATURE",
                                                                               "AVG_HUMIDITY",
                                                                               "AVG_PRESSURE",
                                                                               "AVG_WIND_SPEED",
                                                                               "MOST_COMMON_WEATHER_CODE")
                                SELECT
                                    DATE ("OBSERVED_AT") AS day, "CITY", "LAT", "LON", AVG ("TEMPERATURE"), MIN ("TEMPERATURE"), MAX ("TEMPERATURE"), AVG ("HUMIDITY"), AVG ("PRESSURE"), AVG ("WIND_SPEED"), MODE() WITHIN
                                GROUP (ORDER BY "WEATHER_CODE") AS most_common_weather
                                FROM "WEATHER"."WEATHER_HISTORY"
                                GROUP BY DATE ("OBSERVED_AT"), "CITY", "LAT", "LON"
                                ON CONFLICT ("DAY", "LAT", "LON")
                                    DO
                                UPDATE SET
                                    "AVG_TEMPERATURE" = EXCLUDED."AVG_TEMPERATURE",
                                    "MIN_TEMPERATURE" = EXCLUDED."MIN_TEMPERATURE",
                                    "MAX_TEMPERATURE" = EXCLUDED."MAX_TEMPERATURE",
                                    "AVG_HUMIDITY" = EXCLUDED."AVG_HUMIDITY",
                                    "AVG_PRESSURE" = EXCLUDED."AVG_PRESSURE",
                                    "AVG_WIND_SPEED" = EXCLUDED."AVG_WIND_SPEED",
                                    "MOST_COMMON_WEATHER_CODE" = EXCLUDED."MOST_COMMON_WEATHER_CODE";
                                """)

            conn.commit()

        finally:
            conn.close()

sync_weather_daily()