"""Supervisor routing logic."""
from src.state import GraphState, last_user_message

def supervisor_node(state: GraphState) -> GraphState:
    """Classify a request into software, data, or direct handling."""
    task = last_user_message(state); lowered = task.lower()
    worker = "data_analyst" if any(word in lowered for word in ("csv", "dataset", "data", "estatística", "statistics")) else "software_engineer"
    return {**state, "task": task, "active_worker": worker, "status": "running", "review_loops": state.get("review_loops", 0)}
