"""Constrained Python subprocess execution."""
from __future__ import annotations
import os, subprocess, sys, tempfile
from pathlib import Path
from typing import Any
from src.config import get_settings

def execute_python(code: str, timeout_seconds: int | None = None) -> dict[str, Any]:
    """Execute code in a temporary directory and return structured output."""
    if not code.strip():
        return {"ok": False, "stdout": "", "stderr": "empty code", "returncode": 1}
    timeout = timeout_seconds or get_settings().max_code_seconds
    with tempfile.TemporaryDirectory(prefix="agent-sandbox-") as directory:
        script = Path(directory) / "main.py"
        script.write_text(code, encoding="utf-8")
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"}
        try:
            completed = subprocess.run([sys.executable, str(script)], cwd=directory, env=env, capture_output=True, text=True, timeout=timeout)
            return {"ok": completed.returncode == 0, "stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode}
        except subprocess.TimeoutExpired as exc:
            return {"ok": False, "stdout": exc.stdout or "", "stderr": f"execution timed out after {timeout}s", "returncode": -1}
