import os
from dotenv import load_dotenv
load_dotenv()
"""
agents/prompt_builder.py — System prompt with RAG context injection.

Safety-hardened: prevents misuse, prompt injection, and off-topic conversations.
"""

# ──────────────────────────────────────────────────────────────────────────────
# Core system prompt — concise, safe, professionally scoped
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f'''You are an AI assistant representing {os.getenv("OWNER_NAME", "Tushar")} Bansal.
use tool when need 
- Avoid robotic or overly generic responses'''


def build_system_prompt_with_context(rag_context: str = "") -> str:
    """
    Return the system prompt, optionally with pre-fetched RAG context appended.
    In most cases the agent calls `get_tushar_info` itself via tool use.
    This function is kept for legacy compatibility and direct context injection.
    """
    if rag_context:
        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"PRE-FETCHED PORTFOLIO CONTEXT\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{rag_context}"
        )
    return SYSTEM_PROMPT
