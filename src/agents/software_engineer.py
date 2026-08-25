"""Software engineering agent."""
from src.state import GraphState

def software_engineer_node(state: GraphState) -> GraphState:
    """Produce a transparent engineering artifact for the requested task."""
    task = state.get("task", "")
    artifact = {"type": "engineering", "summary": f"Prepared an implementation plan for: {task}", "code": ""}
    return {**state, "artifacts": state.get("artifacts", []) + [artifact], "status": "review"}
