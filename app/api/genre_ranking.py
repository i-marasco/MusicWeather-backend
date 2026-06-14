"""
-------------------------------------------------------------------------------------------------
genre_ranking.py
-------------------------------------------------------------------------------------------------
Purpose:
        Output genre ranking.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"
        "MUSIC_TRACK"."GENRES"

Inputs:
        start_date[optional]: Start date of genre ranking
        end_date[optional]: End date of genre ranking

Output:
        /weekly:
            Genre weekly ranking.
        /monthly:
            Genre monthly ranking.
"""

from fastapi import APIRouter
from datetime import date, timedelta
from app.services.genre_ranking_services import generate_ranking

router = APIRouter()

@router.post("/weekly")
def weekly():
    today = date.today()

    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=7)

    generate_ranking("WEEKLY", start, end)

    return {"status": "weekly genre ranking generated"}


@router.post("/monthly")
def monthly():
    today = date.today()

    start = today.replace(day=1)
    end = today

    generate_ranking("MONTHLY", start, end)

    return {"status": "monthly genre ranking generated"}