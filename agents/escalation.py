import os
from dotenv import load_dotenv
load_dotenv()
"""
agents/escalation.py — Detects when a visitor needs direct human contact.

No database is used — escalation is purely in-memory / stateless.
When escalation is triggered the agent simply invites the visitor to
send a message via the send_email tool.
"""
from typing import List, Dict, Any

# ──────────────────────────────────────────────────────────────────────────────
# Keyword triggers
# ──────────────────────────────────────────────────────────────────────────────
ESCALATION_KEYWORDS = [
    "talk to tushar", "speak to tushar", "contact tushar",
    "real person", "speak to human", "call me", "phone", "urgent", "asap",
    "not helpful", "confused", "reach out",
]

PROFESSIONAL_SIGNALS = [
    "hire", "hiring", "job offer", "salary", "rate", "freelance",
    "collaboration", "collaborate", "work together", "contract",
]


def should_escalate(user_message: str, rag_chunks: List[Dict[str, Any]]) -> bool:
    """
    Return True when the message should escalate to a human.

    Triggers on:
      - Explicit 'talk to / contact Tushar' requests
      - Professional / hiring inquiries that RAG cannot answer
    """
    msg_lower = user_message.lower()

    if any(kw in msg_lower for kw in ESCALATION_KEYWORDS):
        return True

    # Professional inquiry with no relevant context found
    if not rag_chunks and any(sig in msg_lower for sig in PROFESSIONAL_SIGNALS):
        return True

    return False


def handle_escalation(user_message: str) -> str:
    """
    Return a friendly escalation message inviting the visitor to send an email.
    No database writes — purely stateless.
    """
    return (
        f"It sounds like you'd like to connect with {os.getenv('OWNER_NAME', 'Tushar')} directly! 🙌\n\n"
        f"I can help you send him a message right now. Just share:\n"
        f"1. Your **name**\n"
        f"2. Your **email address**\n"
        f"3. Your **message**\n\n"
        f"And I'll make sure it lands in {os.getenv('OWNER_NAME', 'Tushar')}'s inbox. 📬"
    )
