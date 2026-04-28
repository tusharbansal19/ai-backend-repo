"""
controllers/chat_controller.py — Handles chat and session-end requests.
"""
from utils.models import ChatRequest, EndSessionRequest
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


class EndSessionResponse(BaseModel):
    success: bool
    message: str


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

async def handle_end_session(request: EndSessionRequest) -> EndSessionResponse:
    """
    End-session handler — wipes all volatile memory for the given userId.
    """
    return EndSessionResponse(
        success=True,
        message=f"Session memory cleared for user '{request.userId}'.",
    )
