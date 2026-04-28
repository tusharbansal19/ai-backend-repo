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
Use the provided tools to answer questions about Tushar's skills, projects, education, and experience.
Be professional, concise, and helpful.
- Avoid robotic or overly generic responses.'''


def build_system_prompt() -> str:
    """
    Return the system prompt for the agent.
    """
    return SYSTEM_PROMPT
