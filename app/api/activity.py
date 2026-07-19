"""
-------------------------------------------------------------------------------------------------
activity.py
-------------------------------------------------------------------------------------------------
Purpose:

Source:

Inputs:

Output:

"""

from fastapi import APIRouter
from app.services. activity_services import get_calendar

router = APIRouter()

@router.get("/heatmap")
def get_activity():
    return get_calendar()
