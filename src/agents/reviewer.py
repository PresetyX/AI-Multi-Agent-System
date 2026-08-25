"""Quality assurance reviewer."""
from src.state import GraphState

def reviewer_node(state: GraphState) -> GraphState:
    """Validate artifact presence and finalize or request one bounded retry."""
    artifacts = state.get("artifacts", []); loops = state.get("review_loops", 0)
    if artifacts:
        answer = artifacts[-1].get("summary", "Completed")
        return {**state, "status": "completed", "final_answer": answer, "review_feedback": "approved"}
    return {**state, "status": "failed", "final_answer": "No artifact was produced.", "review_feedback": "missing artifact", "review_loops": loops + 1}
