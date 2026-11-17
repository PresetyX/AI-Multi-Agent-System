import pytest

from src.rag.indexer import index_directory
from src.rag.vector_store import VectorStore
from src.tools.code_executor import execute_python
from src.tools.file_ops import list_workspace, read_workspace_file, write_workspace_file


# ------------------------------------------------------------------ code executor
def test_code_executor_success():
    result = execute_python("print(2 + 2)")
    assert result["ok"] and result["stdout"].strip() == "4"


def test_code_executor_timeout():
    result = execute_python("while True: pass", timeout_seconds=1)
    assert not result["ok"]
    assert result["returncode"] == -1
    assert "timed out" in result["stderr"]


def test_code_executor_rejects_empty_code():
    assert execute_python("   ") == {"ok": False, "stdout": "", "stderr": "empty code", "returncode": 1}


def test_code_executor_reports_errors():
    result = execute_python("raise SystemExit(3)")
    assert not result["ok"] and result["returncode"] == 3


def test_code_executor_does_not_leak_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret")
    result = execute_python("import os; print(os.environ.get('OPENAI_API_KEY'))")
    assert result["stdout"].strip() == "None"


def test_code_executor_runs_in_a_temporary_directory(isolated_workspace):
    result = execute_python("import os; print(os.getcwd())")
    assert "agent-sandbox-" in result["stdout"]


# ------------------------------------------------------------------ file operations
def test_workspace_roundtrip(isolated_workspace):
    write_workspace_file("notes/hello.txt", "hello")
    assert read_workspace_file("notes/hello.txt") == "hello"
    assert (isolated_workspace / "notes" / "hello.txt").exists()  # written to the temp dir only
    assert list_workspace() == ["notes"]


@pytest.mark.parametrize("path", ["../escape.txt", "notes/../../escape.txt", "/etc/passwd"])
def test_workspace_blocks_path_traversal(path):
    with pytest.raises(ValueError, match="escapes workspace"):
        write_workspace_file(path, "x")


# ------------------------------------------------------------------ retrieval
def test_vector_store_ranks_by_token_overlap():
    store = VectorStore()
    store.add_documents(
        [
            {"source": "a.md", "content": "langgraph supervisor routes tasks"},
            {"source": "b.md", "content": "pandas dataframe csv analysis"},
            {"source": "c.md", "content": "langgraph supervisor reviewer loop graph"},
        ]
    )
    results = store.similarity_search("langgraph supervisor reviewer", k=2)
    assert [r["source"] for r in results] == ["c.md", "a.md"]
    assert store.similarity_search("kubernetes") == []


def test_index_directory_only_reads_supported_files(tmp_path):
    (tmp_path / "doc.md").write_text("hello docs", encoding="utf-8")
    (tmp_path / "code.py").write_text("print('hi')", encoding="utf-8")
    (tmp_path / "image.png").write_bytes(b"\x89PNG")
    store = VectorStore()
    assert index_directory(tmp_path, store) == 2
    assert store.similarity_search("hello")[0]["source"].endswith("doc.md")
