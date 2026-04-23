from fastapi import Request
from fastapi.responses import Response
from twilio.rest import Client

from app.agents.orchestrator import orchestrator
from app.db_service import get_or_create_user
from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER
)

# ✅ Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# =========================================
# 🔧 Utility: Split long messages
# =========================================
def split_message(text, limit=1500):
    return [text[i:i + limit] for i in range(0, len(text), limit)]


# =========================================
# 🤖 COMMON PROCESS FUNCTION (USED BY /chat)
# =========================================
async def process_message(message, user_id):
    try:
        # 🔥 DEBUG LOGS
        print("🔥 API HIT")
        print("Message:", message)
        print("User:", user_id)

        # ✅ Validate input
        if not message or not user_id:
            return {"response": "❌ message or user_id missing"}

        # ✅ Ensure WhatsApp format (optional)
        if not str(user_id).startswith("whatsapp:"):
            user_id = f"whatsapp:{user_id}"

        # ✅ Create user in DB
        try:
            get_or_create_user(user_id)
        except Exception as e:
            print("⚠️ DB error:", e)

        # 🧠 Call orchestrator
        reply = orchestrator(user_id, message)

        print("🤖 Reply:", reply)

        # ✅ Fallback if empty
        if not reply:
            reply = "⚠️ No response from AI"

        return {"response": reply}

    except Exception as e:
        print("❌ PROCESS ERROR:", e)
        return {"response": "❌ Internal Server Error"}


# =========================================
# 📲 WHATSAPP WEBHOOK (TWILIO)
# =========================================

async def handle_whatsapp(request: Request):
    try:
        print("🔥 WhatsApp Webhook HIT")

        form = await request.form()

        incoming_msg = form.get("Body")
        user_id = form.get("From")

        print("📩 Incoming:", incoming_msg)
        print("👤 User:", user_id)

        if not incoming_msg or not user_id:
            return Response(content="<Response></Response>", media_type="application/xml")

        if not user_id.startswith("whatsapp:"):
            user_id = f"whatsapp:{user_id}"

        get_or_create_user(user_id)

        # ✅ SAFE CALL
        try:
            reply = orchestrator(user_id, incoming_msg)
            if not reply:
                reply = "⚠️ No response from AI"
        except Exception as e:
            print("❌ Orchestrator Error:", e)
            reply = "❌ AI failed"

        parts = split_message(reply)

        for part in parts:
            client.messages.create(
                body=part,
                from_=TWILIO_WHATSAPP_NUMBER,
                to=user_id
            )

    except Exception as e:
        print("❌ WhatsApp Error:", e)

    return Response(content="<Response></Response>", media_type="application/xml")