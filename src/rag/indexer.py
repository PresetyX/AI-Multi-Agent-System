"""Index text files into the configured retrieval adapter."""
from pathlib import Path
from .vector_store import VectorStore

def index_directory(directory: Path, store: VectorStore | None = None) -> int:
    """Index UTF-8 files recursively and return the number indexed."""
    target = store or VectorStore(); documents = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".py", ".md", ".txt", ".toml"}:
            documents.append({"source": str(path), "content": path.read_text(encoding="utf-8")})
    target.add_documents(documents); return len(documents)
