from app.services.llm_service import generate_response_with_history

# 🧠 Memory storage
user_memory = {}


def run_autogen(user_message: str, user_id: str):
    try:
        print("🔥 AutoGen START")
        print("User:", user_id)
        print("Message:", user_message)

        # Initialize memory
        if user_id not in user_memory:
            user_memory[user_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Reply clearly and briefly. Avoid markdown and code blocks."
                }
            ]

        history = user_memory[user_id]

        # Add user message
        history.append({"role": "user", "content": user_message})

        # Generate response
        response = generate_response_with_history(history)

        # Save response
        history.append({"role": "assistant", "content": response})

        # Limit memory
        user_memory[user_id] = history[-10:]

        return response.strip()

    except Exception as e:
        print("❌ Error:", e)
        return "Something went wrong ❌"
