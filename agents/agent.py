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
@lru_cache(maxsize=1)
def build_llm():
    """
    Lazy load LLM (only once)
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return None

    try:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model="openai/gpt-oss-20b:free",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
    except Exception as e:
        print(f"❌ LLM init error: {e}")
        return None


# ── 2. Build Agent ───────────────────────────────────
@lru_cache(maxsize=1)
def build_agent(prompt: str | None = None):
    """
    Create LangChain ReAct agent with tools
    """
    llm = build_llm()
    if llm is None:
        return None

    try:
        from langgraph.prebuilt import create_react_agent

        agent = create_react_agent(
            model=llm,
            tools=TOOLS,
            prompt="try to give short answer around 50-100 words",
            checkpointer=None
        )

        return agent

    except Exception as e:
        print(f"❌ Agent build error: {e}")
        return None