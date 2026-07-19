"""
-------------------------------------------------------------------------------------------------
dashboard.py
-------------------------------------------------------------------------------------------------
Purpose:
        Populate the dashboard page.

Source:
        "MUSIC_TRACK"."ARTISTS"
        "MUSIC_TRACK"."LISTENING_HISTORY"
        "MUSIC_TRACK"."GENRES"
        "WEATHER"."WEATHER_HISTORY"
Inputs:
        None

Output:
        /dashboard:
        Total track, total artist, total genres, top artist and last weather.
"""

from fastapi import APIRouter
from app.services.dashboard_services import get_dashboard

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    return get_dashboard()
