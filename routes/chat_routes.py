"""
routes/chat_routes.py
POST   /chat          — send a message to the portfolio AI agent
DELETE /chat/session  — end session and wipe volatile memory
"""
from fastapi import APIRouter

from controllers.chat_controller import (
    ChatRequest,
    ChatResponse,
    EndSessionRequest,
    EndSessionResponse,
    handle_chat,
    handle_end_session,
)

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await handle_chat(request)


@router.delete("/session", response_model=EndSessionResponse)
async def end_session(request: EndSessionRequest):
    return await handle_end_session(request)