from datetime import datetime
from pymongo import MongoClient

from src.chat.domain.chat.mongo_schema import MongoChatSchema
from src.chat.domain.chat.chat_models import ChatMessage
from src.chat.domain.chat.conversation_schema import Conversation


class MongoAssistantRepository:
    def __init__(self, uri: str, database_name: str, collection: str):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]
        self.collection = self.database[collection]

    def get_history(self, chat_id: str) -> Conversation:
        chat_history = self.collection.find_one({"chat_id": chat_id})
        if chat_history:
            return Conversation(queries=chat_history["queries"], llm_response=chat_history["llm_response"])
        return Conversation()

    def insert_document(self, doc: ChatMessage) -> None:
        if not doc.chat_id:
            raise ValueError("Chat id is not provided")

        update_document = MongoChatSchema().to_mongo(doc)
        updated_data = {
            "$push": {
                "queries": doc.query,
                "reformulated": doc.summary,
                "sources": {"$each": update_document["sources"]},
                "llm_response": doc.llm_inference,
                "inference_time": doc.inference_time,
                "ir_time": doc.ir_time,
                "prompt_tokens": doc.llm_tokens.prompt_tokens,
                "completion_tokens": doc.llm_tokens.completion_tokens,
            },
            "$set": {
                "updated_at": datetime.now(),
            },
        }

        if self.collection.find_one({"chat_id": doc.chat_id}):
            self.collection.update_one({"chat_id": doc.chat_id}, updated_data)
        else:
            self.collection.insert_one(update_document)
