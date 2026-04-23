from app.services.llm_service import generate_response_with_history


def executor_agent(user_id, plan):
    prompt = f"""
    Execute this plan step by step and give final result.

    Plan:
    {plan}
    """

    response = generate_response_with_history([
        {"role": "user", "content": prompt}
    ])

    return response