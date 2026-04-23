from app.services.llm_service import generate_response_with_history
from app.agents.executor_agent import executor_agent


def planner_agent(user_id, message):
    # Step 1: Plan
    plan_prompt = f"""
    Break this into step-by-step plan:

    {message}
    """

    plan = generate_response_with_history([
        {"role": "user", "content": plan_prompt}
    ])

    # Step 2: Execute
    execution = executor_agent(user_id, plan)

    return f"🧠 Plan:\n{plan}\n\n🚀 Execution:\n{execution}"


