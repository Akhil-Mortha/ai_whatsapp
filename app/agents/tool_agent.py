import requests


def tool_agent(user_id, message):
    try:
        if any(op in message for op in ["+", "-", "*", "/"]):
            return f"🧮 Result: {eval(message)}"
    except:
        pass

    if "weather" in message.lower():
        try:
            res = requests.get("https://wttr.in/?format=3")
            return f"🌤 {res.text}"
        except:
            return "❌ Weather API failed"

    return None