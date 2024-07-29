from pydantic import BaseModel

from src.chat.domain.chat.chat_models import LLMTokens


class TextResponse(BaseModel):
    content: str
    token_count: LLMTokens
    prompt_messages: list[dict[str, str]]
    time: float
