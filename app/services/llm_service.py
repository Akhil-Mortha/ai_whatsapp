import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("🔑 GROQ KEY LOADED:", bool(api_key))

client = Groq(api_key=api_key)


def generate_response_with_history(messages):
    for attempt in range(3):
        try:
            print(f"🔁 Attempt {attempt+1}")

            response = client.chat.completions.create(
                model="llama3-8b-8192", # ✅ stable model
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )

            content = response.choices[0].message.content

            if content:
                print("✅ AI Response OK")
                return content

        except Exception as e:
            print("❌ Groq Error:", e)
            time.sleep(1)

    # ✅ NEVER FAIL
    return "🤖 I'm having a temporary issue. Please try again."

