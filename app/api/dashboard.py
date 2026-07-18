"""
-------------------------------------------------------------------------------------------------
dashboard.py
-------------------------------------------------------------------------------------------------
Purpose:

Source:

Inputs:

Output:
"""

from fastapi import APIRouter
from app.services.dashboard_services import get_dashboard

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    return get_dashboard()
