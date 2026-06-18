from datetime import datetime
import requests
import os
from app.db.conn import get_connection
from dotenv import load_dotenv

load_dotenv()

OPENMETEO_LAT = os.getenv("OPENMETEO_LAT")
OPENMETEO_LON = os.getenv("OPENMETEO_LON")
OPENMETEO_URL = os.getenv("OPENMETEO_URL")

def get_weather_history():
    params = {
        "latitude": OPENMETEO_LAT,
        "longitude": OPENMETEO_LON,
        "start_date": "2025-01-01",
        "end_date": "2026-01-01",
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "auto"
    }

    r = requests.get(OPENMETEO_URL, params=params)
    r.raise_for_status()
    return r.json()


def sync_weather():
    data = get_weather_history()
    hourly = data["hourly"]

    times = hourly["time"]

    conn = get_connection()

    try:
        with conn.cursor() as cur:

            for i in range(len(times)):

                cur.execute("""
                    INSERT INTO "WEATHER"."WEATHER_HISTORY" (
                        "OBSERVED_AT",
                        "CITY",
                        "LAT",
                        "LON",
                        "TEMPERATURE",
                        "HUMIDITY",
                        "PRESSURE",
                        "WIND_SPEED",
                        "WEATHER_CODE"
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """, (
                    datetime.fromisoformat(times[i]),
                    "Milan",
                    float(OPENMETEO_LAT),
                    float(OPENMETEO_LON),

                    hourly["temperature_2m"][i],
                    hourly["relative_humidity_2m"][i],
                    hourly["pressure_msl"][i],
                    hourly["wind_speed_10m"][i],
                    hourly["weather_code"][i]
                ))

            conn.commit()

    finally:
        conn.close()


sync_weather()