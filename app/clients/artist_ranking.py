import psycopg2
from fastapi import APIRouter
from datetime import date, timedelta

API_KEY = "a7955ad0f8a0d65577e476fc67694039"
URL = "https://ws.audioscrobbler.com/2.0/"

router = APIRouter()

def get_connection():
    return psycopg2.connect(
        dbname="music",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

def generate_ranking(period, start_date, end_date):
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


@router.post("/weekly")
def weekly():
    today = date.today()

    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=7)

    generate_ranking("WEEKLY", start, end)

    return {"status": "weekly ranking generated"}

@router.post("/monthly")
def monthly():
    today = date.today()

    start = today.replace(day=1)
    end = today

    generate_ranking("MONTHLY", start, end)

    return {"status": "monthly ranking generated"}