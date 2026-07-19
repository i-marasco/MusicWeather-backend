"""
-------------------------------------------------------------------------------------------------
activity.py
-------------------------------------------------------------------------------------------------
Purpose:
        Output tracks listened per day.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"

Inputs:
        None

Output:
        /activity/heatmap:
        Tracks listened per day and date.

"""

from fastapi import APIRouter
from app.services. activity_services import get_calendar

router = APIRouter()

@router.get("/heatmap")
def get_activity():
    return get_calendar()
