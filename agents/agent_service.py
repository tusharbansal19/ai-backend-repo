from langchain_core.messages import AIMessage
from agents.agent import build_agent
from agents.prompt_builder import build_system_prompt
from agents.escalation import should_escalate, handle_escalation


def process_message(user_message, messages):
    
    # 1. Escalation
    if should_escalate(user_message):
        return AIMessage(content=handle_escalation(user_message))

    # 2. Build system prompt
    system_prompt = build_system_prompt()
    input_messages = messages

    # 3. Get agent
    agent = build_agent(prompt=system_prompt)
    if agent is None:
        return AIMessage(content="LLM unavailable")

    # 4. Invoke agent
    result = agent.invoke({"messages": input_messages})

    final = result["messages"][-1]

    # 5. Always return AIMessage (SAFE)
    return AIMessage(content=final.content)