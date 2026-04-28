from langchain_core.messages import HumanMessage, AIMessage
from agents.agent_service import process_message


def agent_node(state):
    raw_messages = state["messages"]

    messages = []

    for m in raw_messages:
        # ✅ Case 1: Already LangChain object
        if isinstance(m, HumanMessage) or isinstance(m, AIMessage):
            messages.append(m)

        # ✅ Case 2: Dict format
        elif isinstance(m, dict):
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            else:
                messages.append(AIMessage(content=m["content"]))

        else:
            raise ValueError(f"Unsupported message type: {type(m)}")

    # ── Get latest user message ──
    user_message = messages[-1].content

    # ── Process ──
    result = process_message(user_message, messages)

    # ── Return JSON (SAFE) ──
    return {
        "messages": [
            {
                "role": "assistant",
                "content": result.content
            }
        ]
    }