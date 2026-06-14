"""
-------------------------------------------------------------------------------------------------
genres.py
-------------------------------------------------------------------------------------------------
Purpose:
        Output top genres and genres listened per period.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"
        "MUSIC_TRACK"."GENRES"

Inputs:
        start_date[optional]: Start date of genre ranking
        end_date[optional]: End date of genre ranking

Output:
        /top:
            Top genres for the range date selected.
        /period:
            Genres listened per period.
"""

from fastapi import APIRouter, Query
from datetime import datetime
from app.services.genre_service import get_top_genres
from app.services.genre_service import get_genres_by_period

router = APIRouter()

@router.get("/top")
def top_genres(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    return get_top_genres(start_date, end_date)

@router.get("/period")
def genres_by_period(
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    return get_genres_by_period(start_date, end_date)