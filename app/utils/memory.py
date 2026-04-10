user_memory = {}

def save_message(user_id, role, content):
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({
        "role": role,
        "content": content
    })

def get_history(user_id):
    return user_memory.get(user_id, [])
