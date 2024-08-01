from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.completion_usage import CompletionUsage

from langchain_core.messages import AIMessage


class LCConversor:
    @staticmethod
    def to_azure(ai_message: AIMessage) -> ChatCompletion:
        """
        Método custom para traducir la respuesta de LangChain a un ChatCompletion
        """
        openai_message = ChatCompletionMessage(
            content=ai_message.content, role="assistant"
        )

        choice = Choice(
            finish_reason=ai_message.response_metadata.get("finish_reason"),
            index=ai_message.response_metadata.get("index", 0),
            logprobs=ai_message.response_metadata.get("logprobs"),
            message=openai_message,
        )

        usage = CompletionUsage(
            completion_tokens=ai_message.usage_metadata.get("output_tokens"),
            prompt_tokens=ai_message.usage_metadata.get("input_tokens"),
            total_tokens=ai_message.usage_metadata.get("total_tokens"),
        )

        chat_completion = ChatCompletion(
            id=ai_message.id,
            choices=[choice],
            created=0,  # No encuentro dónde aparece este campo en LC
            model=ai_message.response_metadata.get("model_name"),
            object="chat.completion",
            usage=usage,
        )

        return chat_completion
