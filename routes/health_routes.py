"""
routes/health_routes.py — GET /api/health
"""
from fastapi import APIRouter

from config.faiss_store import get_faiss_store

router = APIRouter()


@router.get("")
async def health_check():
    """
    Health check — verifies server, FAISS, and volatile memory status.
    No external database is used in this application.
    """
    # Check FAISS index
    try:
        store = get_faiss_store()
        faiss_docs = int(store.index.ntotal) if store is not None else 0
        faiss_status = "ok"
    except Exception as exc:
        faiss_docs = 0
        faiss_status = f"error: {str(exc)}"

    return {
        "status":        "ok",
        "memory":        "volatile (in-process)",
        "activeSessions": "NA",
        "faiss": {
            "status":     faiss_status,
            "indexDir":   "./faiss_index",
            "documents":  faiss_docs,
        },
    }
