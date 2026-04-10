def tool_agent(user_id, message):
    try:
        if any(op in message for op in ["+", "-", "*", "/"]):
            result = eval(message)
            return f"🧮 Result: {result}"
    except:
        pass

    if "weather" in message.lower():
        return "🌤 Weather: Sunny (demo)"

    return None