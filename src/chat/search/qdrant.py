from time import time

from openai.types.embedding import Embedding
from qdrant_client import QdrantClient

from src.settings.settings import Settings
from src.chat.domain.searcher.searcher_models import Document, SearchResponse


class QdrantSearcher:
    def __init__(self, settings: Settings):
        self.client = QdrantClient(host="localhost", port=6333)

    def search(self, query_emb: Embedding) -> SearchResponse:
        query_emb: list[float] = query_emb.data[0].embedding
        init_time = time()

        search_result = self.client.search(
            collection_name="LangChain-Docs", query_vector=query_emb, limit=1
        )

        out = [
            Document(
                content=search_result.payload["text"],
                title=search_result.payload["title"],
                chunk_id=1,
                score=1,
            )
        ]

        end_time = time()

        return SearchResponse(documents=out, time=end_time - init_time)
