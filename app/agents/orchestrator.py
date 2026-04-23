from app.agents.chat_agent import chat_with_ai
from app.agents.planner_agent import planner_agent
from app.agents.tool_agent import tool_agent
from app.services.llm_service import generate_response_with_history


# 🧠 AI decides which agent to use
def decide_agent(message):
    prompt = f"""
    Decide best agent:
    - planner (for multi-step tasks)
    - tool (for calculations or real-world data)
    - chat (for normal conversation)

    Message: {message}

    Answer only one word.
    """

    res = generate_response_with_history([
        {"role": "user", "content": prompt}
    ])

    return res.strip().lower()


def orchestrator(user_id, message):
    agent = decide_agent(message)

    print("🧠 Agent:", agent)

    if "planner" in agent:
        return planner_agent(user_id, message)

    if "tool" in agent:
        tool_result = tool_agent(user_id, message)
        if tool_result:
            return tool_result

    return chat_with_ai(user_id, message)