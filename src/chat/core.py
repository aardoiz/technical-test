from openai.types.embedding import Embedding

from src.settings.settings import Settings
from src.chat.domain.chat.chat_models import ChatMessage, LLMTokens
from src.chat.domain.chat.conversation_schema import Conversation
from src.chat.domain.generation.text_models import TextResponse
from src.chat.domain.searcher.searcher_models import SearchResponse
from src.chat.generation.agents.assistant import Assistant
from src.chat.generation.agents.reformulator import Reformulator
from src.chat.generation.agents.planner import Planner
from src.chat.generation.llm_clients.gpt import AzureClient
from src.chat.search.qdrant import QdrantSearcher
from src.chat.search.arxiv import ArxivAPI


class Core:
    def __init__(self, settings: Settings):
        self.llm = AzureClient(settings)
        self.searcher = QdrantSearcher(settings)
        self.reformulator = Reformulator(self.llm)
        self.assistant = Assistant(self.llm)
        self.planner = Planner(self.llm)
        self.arxivAPI = ArxivAPI()

    def deus_ex_chat(
        self, chat_id: str, query: str, conversation: Conversation
    ) -> ChatMessage:
        complex_query: TextResponse = self.reformulator.reformulate(query, conversation)

        planner_result: TextResponse = self.planner.select_agent(query=complex_query)

        if "General" in planner_result.content:
            context = SearchResponse(documents=[], time=0.0, sources=[])

        elif "Arxiv" in planner_result.content:
            complex_query: TextResponse = self.reformulator.ir_reformulate(query)
            context: SearchResponse = self.arxivAPI.search(complex_query.content)

        elif "Docu" in planner_result.content:
            query_embedding: Embedding = self.llm.generate_embedding(
                complex_query.content
            )
            context: SearchResponse = self.searcher.search(query_embedding)

        answer: TextResponse = self.assistant.answer_query(
            complex_query.content, conversation, context.documents
        )

        p_tokens = answer.token_count.prompt_tokens
        c_tokens = answer.token_count.completion_tokens

        return ChatMessage(
            chat_id=chat_id,
            query=query,
            agent=planner_result.content,
            summary=complex_query.content,
            sources=context.sources,
            inference_time=answer.time,
            ir_time=context.time,
            llm_inference=answer.content,
            llm_tokens=LLMTokens(prompt_tokens=p_tokens, completion_tokens=c_tokens),
        )
