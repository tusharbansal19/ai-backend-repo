import os
from dotenv import load_dotenv
load_dotenv()
"""
main.py — FastAPI application entry point
Portfolio AI Backend (FREE stack: HuggingFace + ChromaDB, no external DB)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from utils.error_handler import global_exception_handler
from utils.rate_limiter import rate_limit_middleware
from routes.chat_routes import router as chat_router
from routes.health_routes import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # No database to connect — ChromaDB initialises lazily on first query.
    # Memory is purely in-process (volatile dict in memory/memory_manager.py).
    yield


app = FastAPI(
    title="Portfolio AI Backend",
    description=(
        "AI Agent for Tushar Bansal's portfolio. "
        "Powered by LangGraph ReAct + ChromaDB RAG + HuggingFace. "
        "No external database required."
    ),
    version="2.0.0",
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

app.include_router(chat_router,   prefix="/api/chat",   tags=["Chat"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
    )
