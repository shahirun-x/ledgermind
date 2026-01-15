from fastapi import APIRouter
from pydantic import BaseModel

from app.services.intent_parser import parse_intent
from app.services.executor import execute_intent

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    intent = parse_intent(request.question)
    answer = execute_intent(intent)
    return ChatResponse(answer=answer)
