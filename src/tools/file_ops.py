"""Workspace-restricted file operations."""
from pathlib import Path
from src.config import get_settings

def _safe_path(relative_path: str) -> Path:
    root = get_settings().workspace_root.resolve(); root.mkdir(parents=True, exist_ok=True)
    target = (root / relative_path).resolve()
    if target != root and root not in target.parents: raise ValueError("path escapes workspace")
    return target

def read_workspace_file(relative_path: str) -> str:
    """Read UTF-8 text from workspace."""
    return _safe_path(relative_path).read_text(encoding="utf-8")

def write_workspace_file(relative_path: str, content: str) -> str:
    """Write UTF-8 text into workspace and return its relative path."""
    target = _safe_path(relative_path); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(content, encoding="utf-8"); return relative_path

def list_workspace(relative_path: str = ".") -> list[str]:
    """List immediate workspace entries."""
    target = _safe_path(relative_path); return sorted(item.name for item in target.iterdir())
