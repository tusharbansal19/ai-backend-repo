import asyncio
from graph.builder import graph

async def run_agent(user_id: str, user_message: str):
    result = await asyncio.to_thread(
        graph.invoke,
        {
            "messages": [
                {"role": "user", "content": user_message}
            ]
        },
        config={
            "configurable": {
                "thread_id": user_id
            }
        },
    )

    final = result["messages"][-1]

    # `final` is now a LangChain message (like AIMessage) because we use add_messages
    reply_content = getattr(final, "content", "") if hasattr(final, "content") else final.get("content", "")

    return {
        "reply": reply_content,
        "toolCalled": None,
        "toolResult": None,
        "metadata": {
            "model": "openrouter-free-langgraph"
        }
    }