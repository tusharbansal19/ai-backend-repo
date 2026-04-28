"""
config/llm_client.py — HuggingFace LLM (gemma-3-27b-it) via LangChain (FREE)
Pattern matches your existing working code exactly.
"""
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# OpenRouter Configuration (LangGraph-compatible)
llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)
