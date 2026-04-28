"""
controllers/chat_controller.py — Handles chat and session-end requests.
"""
from utils.models import ChatRequest
from agents.runAgent import run_agent
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────────────────────────────────────
# Response models
# ──────────────────────────────────────────────────────────────────────────────
class ChatResponse(BaseModel):
    reply:      str
    toolCalled: str  | None = None
    toolResult: dict | None = None
    escalated:  bool        = False
    metadata:   dict        = Field(default_factory=dict)


# ──────────────────────────────────────────────────────────────────────────────
# Handlers
# ──────────────────────────────────────────────────────────────────────────────
async def handle_chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat handler — validates input, runs the LangGraph agent,
    returns a structured response.
    """
    result = await run_agent(
        user_id=request.userId,
        user_message=request.message,
    )
    return ChatResponse(
        reply      = result["reply"],
        toolCalled = result.get("toolCalled"),
        toolResult = result.get("toolResult"),
        escalated  = result.get("escalated", False),
        metadata   = result.get("metadata", {}),
    )

async def handle_clear_session(user_id: str) -> dict:
    """
    Clears session for a specific user ID.
    """
    from graph.builder import clear_session
    clear_session(user_id)
    return {"success": True, "message": f"Session for {user_id} removed."}


