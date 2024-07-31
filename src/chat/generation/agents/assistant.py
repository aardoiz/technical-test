from time import time

from openai.types.chat.chat_completion import ChatCompletion

from src.chat.domain.chat.conversation_schema import Conversation
from src.chat.domain.generation.text_models import TextResponse
from src.chat.domain.searcher.searcher_models import Document
from src.chat.domain.chat.chat_models import LLMTokens
from src.chat.generation.llm_clients.gpt import AzureClient


class Assistant:
    def __init__(self, llm: AzureClient):
        self.base_instruction = {
            "role": "system",
            "content": "Eres un asistente especializado en dominio general. "
            "Responde a las peticiones de los usuarios usando tu conocimiento.\
             De forma complementaria usa los documentos que te pasan como contexto si es necesario."
            "Los documentos pueden venir de Arxiv, o ser una página de documentación de Langchain."
            "Cuando utilices un documento, referencia en la respuesta el título del documento que estás usando."
            "Procura responder de una manera sencilla, ordenada y basándote en evidencias. "
            "La precisión y calidad de tus respuestas es de vital importancia. "
            "La información contenida en los documentos de contexto puede ser irrelevante."
            "Responde en el mismo idioma del usuario, es decir, si te pregunta en inglés, \
             responde en inglés.",
        }
        self.llm_client = llm

    @staticmethod
    def build_context(docs: list[Document]) -> str:
        prompt = "Documentos como Contexto:\n"
        for doc in docs:
            prompt += f"\nTítulo:{doc.title} -> {doc.content}"
        return prompt

    def construct_history(
        self, user_query: str, conversation: Conversation, docs: str
    ) -> list[dict[str, str]]:
        history = []

        for idx, query in enumerate(conversation.queries):
            history.append({"role": "user", "content": query})
            history.append(
                {"role": "assistant", "content": conversation.llm_response[idx]}
            )

        history.insert(0, self.base_instruction)
        history.append({"role": "system", "content": docs})
        history.append({"role": "user", "content": user_query})

        return history

    def answer_query(
        self, query: str, conversation: Conversation, documents: list[Document]
    ) -> TextResponse:
        i_time = time()

        context = self.build_context(documents)
        history = self.construct_history(query, conversation, context)

        llm_response: ChatCompletion = self.llm_client.generate(
            history, temperature=0.0, max_tokens=2000
        )

        e_time = time()

        return TextResponse(
            content=llm_response.choices[0].message.content,
            token_count=LLMTokens(
                prompt_tokens=llm_response.usage.prompt_tokens,
                completion_tokens=llm_response.usage.completion_tokens,
            ),
            prompt_messages=history,
            time=(e_time - i_time),
        )
