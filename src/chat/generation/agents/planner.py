from openai.types.chat.chat_completion import ChatCompletion
from time import time

from src.chat.domain.generation.text_models import TextResponse
from src.chat.domain.chat.chat_models import LLMTokens
from src.chat.generation.llm_clients.gpt import AzureClient
from src.chat.domain.chat.conversation_schema import Conversation
from src.chat.domain.generation.text_models import TextResponse



class Planner:

    def __init__(self, llm: AzureClient):
        self.llm_client = llm

    def build_history(self, conversation: Conversation) -> list[dict[str, str]]:
        history = []
        for idx, query in enumerate(conversation.queries):
            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": conversation.llm_response[idx]})

        return history

    def reformulate(self, query: str, conversation: Conversation) -> TextResponse:
        i_time = time()
        history = self.build_history(conversation)
        if not history:
            return TextResponse(content=query, token_count=LLMTokens(), prompt_messages=[], time=0)

        messages = [
            {
                "role": "system",
                "content": "Eres un sistema de apoyo para un Asistente basado en LLMs."
                "Tu función es reformular la última query del usuario para incluir en ella el contexto necesario "
                "para hacerla posible de entender en un único mensaje."
                "Utiliza toda la conversación para intentar que la query reformulada sea lo más completa posible."
                "En caso de que no sea necesario reformular la última query, déjala tal y como está.",
            },
            {
                "role": "system",
                "content": 'Utiliza el siguiente ejemplo como base: CONVERSACIÓN: {"role": "assistant", "content":'
                '"Hola, ¿cómo te puedo ayudar?"}, '
                '{"role": "user", "content": "Cuál es la clínica veterinaria más grande de madrid?"},'
                ' {"role": "assistant", '
                '"content": "La clínica veterinaria de Madrid más grande es la de calle ferraz"}, {"role": "user", '
                '"content": "Y en barcelona?"}',
            },
            {
                "role": "assistant",
                "content": "REFORMULATED QUERY: Cuál es la clínica veterinaria más grande de Barcelona?",
            },
            {
                "role": "user",
                "content": f"Reformula la siguiente query: {query} usando la conversación pasada. "
                f"CONVERSACIÓN: {history}\n\nREFORMULATED QUERY:",
            },
        ]

        llm_response: ChatCompletion = self.llm_client.generate(messages, temperature=0.0, max_tokens=1000)

        text_response = llm_response.choices[0].message.content
        e_time = time()

        return TextResponse(
            content=text_response,
            token_count=LLMTokens(
                prompt_tokens=llm_response.usage.prompt_tokens,
                completion_tokens=llm_response.usage.completion_tokens,
            ),
            prompt_messages=messages,
            time=(e_time - i_time),
        )
