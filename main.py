print("DEBUG: main.py is being loaded...")
import os
from dotenv import load_dotenv
load_dotenv()
print("STARTING APP...")
print(f"DEBUG: Environment loaded. PORT={os.getenv('PORT')}")
print(f"DEBUG: OWNER_NAME: {os.getenv('OWNER_NAME', 'NOT SET')}")

"""
main.py — FastAPI application entry point for the portfolio assistant.
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from routes.chat_routes import router as chat_router
    from routes.health_routes import router as health_router
    print("Imports successful [OK]")
except Exception as e:
    print("IMPORT ERROR [FAIL]:", e)
    raise e

from utils.error_handler import global_exception_handler
from utils.rate_limiter import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    LAZY LOADING STRATEGY:
    We no longer pre-load models or FAISS here. 
    This allows the app to start instantly on Render free tier 
    without hitting the 30s timeout or 512MB RAM limit during startup.
    Models will load on the first request instead.
    """
    print("DEBUG: Lifespan starting (Fast Startup Mode)...")
    print("Models will be lazy-loaded on the first request to save memory.")
    
    # Optional: You can still check if FAISS index exists on disk without loading it
    from config.faiss_store import _index_path
    index_dir = _index_path()
    if not (index_dir / "index.faiss").exists():
        print("WARNING: FAISS index not found on disk. Ingestion may be needed later.")
    else:
        print("DEBUG: FAISS index detected on disk.")

    yield
    print("DEBUG: Lifespan ending...")


app = FastAPI(
    title="Portfolio AI Backend",
    description="AI assistant for Tushar Bansal's portfolio, powered by FastAPI, LangGraph, and RAG.",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.middleware("http")(rate_limit_middleware)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(health_router, prefix="/health", tags=["Health"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
    )