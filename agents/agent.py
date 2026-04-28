"""
agents/agent.py

Responsible ONLY for:
- Building LLM
- Building LangChain Agent

No business logic here.
"""

import os
from functools import lru_cache

from tools.langchain_tools import TOOLS


# ── 1. Build LLM ─────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()

def build_llm():
    """
    Build the LLM instance using OpenRouter.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Add it in your .env file."
        )

    try:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model="openai/gpt-oss-20b:free",
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
    except Exception as e:
        print(f"❌ LLM init error: {e}")
        return None


# ── 2. Build Agent ───────────────────────────────────
def build_agent(prompt: str | None = None):
    """
    Create LangChain ReAct agent with tools
    """
    llm = build_llm()
    if llm is None:
        return None

    try:
        from langgraph.prebuilt import create_react_agent

        # Use the passed system prompt or a default one
        system_prompt = prompt or "You are a helpful AI assistant."

        agent = create_react_agent(
            model=llm,
            tools=TOOLS,
            state_modifier=system_prompt,
            checkpointer=None
        )

        return agent

    except Exception as e:
        print(f"❌ Agent build error: {e}")
        return None