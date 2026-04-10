from app.services.llm_service import generate_response_with_history
from app.services.rag_service import store_message, retrieve_context


def chat_with_ai(user_id, message):
    past_context = retrieve_context(user_id, message)

    messages = []

    for msg in past_context:
        messages.append({"role": "user", "content": msg})

    messages.append({"role": "user", "content": message})

    response = generate_response_with_history(messages)

    store_message(user_id, message)
    store_message(user_id, response)

    return response