"""Shared graph state and message helpers."""
from typing import Any, Literal, TypedDict

class GraphState(TypedDict, total=False):
    """Serializable state passed between LangGraph nodes."""
    messages: list[dict[str, str]]
    active_worker: str
    task: str
    artifacts: list[dict[str, Any]]
    tool_history: list[dict[str, Any]]
    status: Literal["pending", "running", "review", "completed", "failed"]
    review_feedback: str
    review_loops: int
    final_answer: str

def last_user_message(state: GraphState) -> str:
    """Extract the latest user content."""
    for message in reversed(state.get("messages", [])):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""
