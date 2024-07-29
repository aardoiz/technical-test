from pydantic import BaseModel


class Document(BaseModel):
    content: str
    title: str
    chunk_id: str
    score: float


class SearchResponse(BaseModel):
    documents: list[Document]
    time: float
