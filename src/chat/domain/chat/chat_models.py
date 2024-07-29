from pydantic import BaseModel

from src.chat.domain.searcher.searcher_models import SearchResponse


class LLMTokens(BaseModel):
    prompt_tokens: int
    completion_tokens: int


class ChatMessage(BaseModel):

    chat_id: str
    query: str
    summary: str
    sources: SearchResponse
    llm_inference: str
    inference_time: float
    ir_time: float
    external_api_time: float
    llm_tokens: LLMTokens

class Conversation(BaseModel):

    queries: list[str] = []
    llm_response: list[str] = []
