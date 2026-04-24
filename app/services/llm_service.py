import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found")

client = Groq(api_key=api_key)


def generate_response_with_history(messages):
    import time

    for attempt in range(3):
        try:
            print(f"🔁 LLM attempt {attempt+1}")

            response = client.chat.completions.create(
                model="llama3-8b-8192", # ✅ more stable model
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )

            content = response.choices[0].message.content

            if content:
                print("✅ LLM Success")
                return content

        except Exception as e:
            print(f"❌ Groq Error (attempt {attempt+1}):", e)
            time.sleep(1)

    # ✅ FINAL FALLBACK (VERY IMPORTANT)
    return "🤖 I'm facing a temporary issue, please try again."

