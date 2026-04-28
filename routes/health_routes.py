"""
routes/health_routes.py — GET /api/health
"""
from fastapi import APIRouter



router = APIRouter()


@router.get("")
async def health_check():
    """
    Health check — verifies server status.
    """
    return {
        "status": "ok",
        "message": "Portfolio AI Backend is running smoothly."
    }
