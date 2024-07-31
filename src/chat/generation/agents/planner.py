import json
from openai.types.chat.chat_completion import ChatCompletion
from time import time

from src.chat.domain.generation.text_models import TextResponse
from src.chat.domain.chat.chat_models import LLMTokens
from src.chat.generation.llm_clients.gpt import AzureClient


class Planner:
    def __init__(self, llm: AzureClient):
        self.llm_client = llm

    def select_agent(self, query: str) -> TextResponse:
        i_time = time()

        messages = [
            {
                "role": "system",
                "content": "Eres un sistema de apoyo para un Asistente basado en LLMs."
                "Tu función es planificar que agentes son necesarios para el flujo del sistema."
                "Actualmente hay tres agentes: 1. Docu: Una base de datos de documentación sobre LangChain \
                2. Arxiv: Un conector a Arxiv para búsquedas bibliográficas 3. General: Un asistente general."
                'Debes devolver un json que siga el siguiente formato: {"agente": agente que debería usarse en \
                función a la query del usuario (Docu/Arxiv/General)}'
                "Hazlo correctamente y serás recompensado.",
            },
            {
                "role": "user",
                "content": f"Qué agente es necesario para responder la siguiente query: {query}",
            },
        ]

        llm_response: ChatCompletion = self.llm_client.generate(
            messages, temperature=0.0, max_tokens=1000
        )

        text_response = self.get_value(llm_response.choices[0].message.content)
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

    @staticmethod
    def get_value(data_string):
        json_str = data_string.strip("```json\n").strip("\n```")
        data = json.loads(json_str)
        agent_value = data["agente"]

        return agent_value
