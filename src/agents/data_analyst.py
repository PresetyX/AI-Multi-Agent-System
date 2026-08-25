"""Data analysis agent."""
from src.state import GraphState

def data_analyst_node(state: GraphState) -> GraphState:
    """Produce a structured analysis artifact without inventing unavailable data."""
    task = state.get("task", "")
    artifact = {"type": "data_analysis", "summary": f"Prepared an analysis plan for: {task}", "findings": []}
    return {**state, "artifacts": state.get("artifacts", []) + [artifact], "status": "review"}
