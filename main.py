import os
from dotenv import load_dotenv
load_dotenv()
"""
main.py — FastAPI application entry point for the portfolio assistant.
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat_routes import router as chat_router
from routes.health_routes import router as health_router
from utils.error_handler import global_exception_handler
from utils.rate_limiter import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing models and FAISS datastore...")
    from rag.embedder import get_embedding_model
    from config.faiss_store import get_faiss_store
    from scripts.ingest_documents import ingest
    
    # These functions use @lru_cache, so calling them here pre-loads them into memory
    get_embedding_model()
    
    # Load FAISS. If it doesn't exist yet, ingest data
    store = get_faiss_store()
    if store is None:
        print("FAISS index not found. Ingesting documents...")
        ingest()
        # Ingestion saved the index, so clear the lru_cache and load it again
        get_faiss_store.cache_clear()
        get_faiss_store()
        
    print("Models and datastore loaded into memory.")
    yield


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