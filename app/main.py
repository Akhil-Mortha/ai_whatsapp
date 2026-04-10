from fastapi import FastAPI
from pydantic import BaseModel

from app.services.autogen_service import run_autogen
from app.db_service import get_or_create_user, save_message, get_messages

app = FastAPI()


# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str
    user_id: str


# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "🚀 AI Backend Running Successfully"}


# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    # 🔐 Ensure user exists
    user_id = get_or_create_user(req.user_id)

    # 💾 Save user message
    save_message(user_id, "user", req.message)

    # 🧠 Get chat history (optional for memory)
    history = get_messages(user_id)

    # 🤖 Generate AI response (Groq via AutoGen service)
    reply = run_autogen(req.message, user_id)

    # 💾 Save assistant response
    save_message(user_id, "assistant", reply)

    return {
        "response": reply,
        "user_id": user_id
    }


# =========================
# DEBUG ENDPOINT (optional)
# =========================
@app.get("/history/{user_id}")
def history(user_id: str):
    return get_messages(user_id)

