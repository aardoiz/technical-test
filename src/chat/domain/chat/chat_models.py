from pydantic import BaseModel

from src.chat.domain.searcher.searcher_models import Source


class LLMTokens(BaseModel):
    prompt_tokens: int
    completion_tokens: int


class ChatMessage(BaseModel):
    chat_id: str
    query: str
    agent: str
    summary: str
    sources: list[Source]
    llm_inference: str
    inference_time: float
    ir_time: float
    llm_tokens: LLMTokens


class Conversation(BaseModel):
    queries: list[str] = []
    llm_response: list[str] = []
