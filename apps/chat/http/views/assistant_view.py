from apps.chat.boot import boot
from apps.chat.http.schemas.models import AssistantInput
from src.chat.domain.chat.chat_models import ChatMessage
from src.chat.domain.chat.conversation_schema import Conversation
from src.shared.logger import logger


def process_text_view(query: AssistantInput) -> ChatMessage:
    logger.info(f"Processing query from {query.chat_id}")

    history: Conversation = boot.repository.get_history(query.chat_id)
    result: ChatMessage = boot.core.deus_ex_chat(query.chat_id, query.query, history)

    boot.repository.insert_document(result)

    return result
