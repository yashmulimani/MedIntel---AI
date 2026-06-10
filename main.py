from fastapi import FastAPI

from agents.chatbot import get_chat_response

from schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)

app = FastAPI(title="MedIntel API", version="1.0.0")

@app.get("/")
def home():
    return {"message": "Welcome to MedIntel API"}

@app.post("/chat", response_model = ChatResponse)
def chat(request: ChatRequest):
    response = get_chat_response(
        message = request.message,
        thread_id = request.thread_id
    )

    return ChatResponse(response=response)