"""Optional Chroma vector-store wrapper with a deterministic fallback."""
from pathlib import Path
from typing import Any
from src.config import get_settings

class VectorStore:
    """Small adapter that avoids requiring provider credentials for tests."""
    def __init__(self, persist_directory: Path | None = None) -> None:
        self.persist_directory = persist_directory or get_settings().rag_persist_directory
        self._documents: list[dict[str, str]] = []
    def add_documents(self, documents: list[dict[str, str]]) -> None:
        """Add documents to the in-process fallback index."""
        self._documents.extend(documents)
    def similarity_search(self, query: str, k: int = 4) -> list[dict[str, Any]]:
        """Return simple token-overlap results; production can replace with Chroma."""
        tokens = set(query.lower().split())
        scored = [(len(tokens & set(doc.get("content", "").lower().split())), doc) for doc in self._documents]
        return [doc for score, doc in sorted(scored, key=lambda item: item[0], reverse=True)[:k] if score > 0]
