from datetime import datetime

from src.chat.domain.chat.chat_models import ChatMessage
from src.chat.domain.chat.conversation_schema import Conversation


class MongoChatSchema:
    @staticmethod
    def to_mongo(doc: ChatMessage) -> dict:
        return {
            "chat_id": doc.chat_id,
            "queries": [doc.query],
            "reformulated": [doc.summary],
            "agent": [doc.agent],
            "sources": [
                [
                    {"title": source.title, "score": source.score}
                    for source in doc.sources
                ]
            ],
            "llm_response": [doc.llm_inference],
            "inference_time": [doc.inference_time],
            "ir_time": [doc.ir_time],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "prompt_tokens": [doc.llm_tokens.prompt_tokens],
            "completion_tokens": [doc.llm_tokens.completion_tokens],
        }

    @staticmethod
    def to_domain(doc: dict) -> Conversation:
        return Conversation(**doc)
