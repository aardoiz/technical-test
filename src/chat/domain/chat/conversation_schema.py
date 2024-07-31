from pydantic import BaseModel


class Conversation(BaseModel):
    queries: list[str] = []
    llm_response: list[str] = []
