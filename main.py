print("DEBUG: main.py is being loaded (ULTRA-LIGHT MODE)...")
import os
from dotenv import load_dotenv
load_dotenv()
print("STARTING APP...")

"""
main.py — FastAPI application entry point for the portfolio assistant.
Optimized for 512MB RAM / 30s timeout environments (Render Free Tier).
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DEBUG: Lifespan starting (Lazy Startup)...")
    # No heavy work here. Models and Data will load when the first API call happens.
    yield
    print("DEBUG: Lifespan ending...")

app = FastAPI(
    title="Portfolio AI Backend",
    description="AI assistant for Tushar Bansal's portfolio.",
    version="3.1.0",
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

# ── LAZY ROUTE INJECTION ───────────────────────────────────────────────────
# We define wrapper endpoints to avoid importing the entire LangChain stack at boot.

@app.post("/chat")
async def chat_proxy(request: dict):
    from controllers.chat_controller import handle_chat, ChatRequest
    return await handle_chat(ChatRequest(**request))

@app.delete("/chat/session")
async def end_session_proxy(request: dict):
    from controllers.chat_controller import handle_end_session, EndSessionRequest
    return await handle_end_session(EndSessionRequest(**request))

@app.get("/health")
async def health_proxy():
    from routes.health_routes import health_check
    return await health_check()

# ── ERROR HANDLING ─────────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    print(f"CRITICAL ERROR: {exc}")
    return JSONResponse(status_code=500, content={"success": False, "error": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False
    )