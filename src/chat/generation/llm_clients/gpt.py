import openai

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.embedding import Embedding

from src.settings.settings import Settings
from src.chat.domain.generation.langchain_conversor import LCConversor


class AzureClient:
    def __init__(self, settings: Settings) -> None:
        self.client = openai.AzureOpenAI(
            azure_endpoint=settings.AZURE_API_BASE,
            api_key=settings.AZURE_API_KEY,
            api_version=settings.AZURE_API_VERSION,
        )
        self.deployment = settings.AZURE_API_DEPLOYMENT
        self.embeddings = settings.AZURE_API_EMBEDDINGS

    def generate(
        self, message_history: list[dict], temperature: float, max_tokens: int
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            messages=message_history,
            model=self.deployment,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=69,
        )

    def generate_embedding(self, text: str) -> Embedding:
        embedding = self.client.embeddings.create(model=self.embeddings, input=text)
        return embedding


class LangChainAzure:
    def __init__(self, settings: Settings) -> None:
        self.client = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_API_BASE,
            azure_deployment=settings.AZURE_API_DEPLOYMENT,
            openai_api_version=settings.AZURE_API_VERSION,
            api_key=settings.AZURE_API_KEY,
        )
        self.conversor = LCConversor()

    def generate(
        self, message_history: list[dict], temperature: float, max_tokens: int
    ) -> ChatCompletion:
        response: AIMessage = self.client.with_config(
            configurable={
                "llm_temperature": temperature,
                "max_tokens": max_tokens,
                "seed": 69,
            }
        ).invoke(message_history)

        return self.conversor.to_azure(response)

    def generate_embedding(self, text: str) -> Embedding: ...
