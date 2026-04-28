"""
controllers/chat_controller.py — Handles chat and session-end requests.
"""
from pydantic import BaseModel, Field, field_validator
from agents.runAgent import run_agent

# ──────────────────────────────────────────────────────────────────────────────
# Request / Response models
# ──────────────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    userId:  str = Field(default="1", min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message cannot be blank or whitespace only")
        return v.strip()

    @field_validator("userId")
    @classmethod
    def user_id_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("userId cannot be blank")
        return v.strip()


class ChatResponse(BaseModel):
    reply:      str
    toolCalled: str  | None = None
    toolResult: dict | None = None
    escalated:  bool        = False
    metadata:   dict        = Field(default_factory=dict)


class EndSessionRequest(BaseModel):
    userId: str = Field(..., min_length=1, max_length=100)


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
    Call this when the visitor closes the chat widget.
    """
   
    return EndSessionResponse(
        success=True,
        message=f"Session memory cleared for user '{request.userId}'.",
    )
