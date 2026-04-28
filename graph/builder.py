# graph/builder.py

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
import sqlite3
from pathlib import Path

from graph.nodes import agent_node

# ── State ─────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


checkpointer = MemorySaver()


# ── Graph builder ─────────────────────────────────────
builder = StateGraph(AgentState)

print("graph executing......")

builder.add_node("agent", agent_node)
print("graph executiing agents ends......")

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile(checkpointer=checkpointer)