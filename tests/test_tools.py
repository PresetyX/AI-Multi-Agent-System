from src.tools.code_executor import execute_python
from src.tools.file_ops import write_workspace_file, read_workspace_file

def test_code_executor_success():
    result = execute_python("print(2 + 2)")
    assert result["ok"] and result["stdout"].strip() == "4"

def test_code_executor_timeout():
    result = execute_python("while True: pass", timeout_seconds=1)
    assert not result["ok"]

def test_workspace_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("WORKSPACE_ROOT", str(tmp_path))
    write_workspace_file("hello.txt", "hello")
    assert read_workspace_file("hello.txt") == "hello"
