from fastapi import APIRouter

from apps.chat.http.schemas.models import AssistantInput
from apps.chat.http.views.assistant_view import process_text_view
from src.chat.domain.chat.chat_models import ChatMessage

chat_router = APIRouter()


@chat_router.post("/chat", response_model=ChatMessage)
def assistant_answer(query: AssistantInput):
    return process_text_view(query)
