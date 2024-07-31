import httpx
from lxml import etree
from time import time

from src.chat.domain.searcher.searcher_models import Document, SearchResponse, Source


class ArxivAPI:
    def __init__(self):
        self.max_results: int = 5
        self.sort_by: str = "submittedDate"
        self.sort_order: str = "descending"

    def search(self, query: str) -> SearchResponse:
        init_time = time()
        xml_raw = self.get_data(query)
        documents = self.parse_xml(xml_raw)
        sources = self.clean_sources(documents)

        return SearchResponse(
            documents=documents, time=time() - init_time, sources=sources
        )

    def get_data(self, query: str) -> str:
        base_url = f"http://export.arxiv.org/api/query?search_query=all:{query}"
        filters = f"&start=0&max_results={self.max_results}&sortBy={self.sort_by}&sortOrder={self.sort_order}"
        url = f"{base_url}{filters}"

        with httpx.Client() as client:
            response = client.get(url)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to get data from arXiv: {response.status_code}")

    @staticmethod
    def parse_xml(xml_data: str) -> list[Document]:
        root = etree.fromstring(xml_data.encode())
        namespace_map = {"": "http://www.w3.org/2005/Atom"}

        documents = []

        for i, entry in enumerate(root.findall(".//entry", namespaces=namespace_map)):
            title = entry.find("./title", namespaces=namespace_map).text.strip()
            summary = entry.find("./summary", namespaces=namespace_map).text.strip()

            score = 1 - (i * 0.1)

            document = Document(
                content=summary, title=title, score=score, chunk_id=f"{i}"
            )

            documents.append(document)

        return documents

    @staticmethod
    def clean_sources(docs: list[Document]) -> list[Source]:
        sources = []
        for doc in docs:
            sources.append(Source(title=doc.title, score=doc.score))

        return sources
