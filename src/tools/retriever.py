"""Retrieval facade over the local RAG index."""
from typing import Any
from src.rag.vector_store import VectorStore

def retrieve_documents(query: str, k: int = 4) -> list[dict[str, Any]]:
    """Retrieve relevant internal documents, returning empty results if unconfigured."""
    return VectorStore().similarity_search(query, k=k)
