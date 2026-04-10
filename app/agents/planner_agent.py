from app.services.llm_service import generate_response_with_history

def planner_agent(user_id, message):
    prompt = f"""
Break the user request into step-by-step plan.

User: {message}
"""

    response = generate_response_with_history([
        {"role": "user", "content": prompt}
    ])

    return f"🧠 Plan:\n{response}"