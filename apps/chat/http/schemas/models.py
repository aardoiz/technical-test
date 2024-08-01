from pydantic import BaseModel

from src.chat.domain.chat.chat_models import ChatMessage


class AssistantInput(BaseModel):
    query: str
    chat_id: str


class AssistantOutput(BaseModel):
    result: ChatMessage
