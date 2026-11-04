"""LangGraph workflow construction."""
from langgraph.graph import END, START, StateGraph
from src.config import get_settings
from src.state import GraphState
from src.agents.supervisor import supervisor_node
from src.agents.software_engineer import software_engineer_node
from src.agents.data_analyst import data_analyst_node
from src.agents.reviewer import reviewer_node

def route_worker(state: GraphState) -> str:
    """Select the worker chosen by the supervisor."""
    return state.get("active_worker", "software_engineer")

def route_review(state: GraphState) -> str:
    """Return terminal outcome, with a bounded fallback to supervisor."""
    if state.get("status") == "completed": return "done"
    if state.get("review_loops", 0) < get_settings().max_review_loops: return "retry"
    return "done"

def build_graph():
    """Compile the stateful multi-agent graph."""
    graph = StateGraph(GraphState)
    graph.add_node("supervisor", supervisor_node); graph.add_node("software_engineer", software_engineer_node); graph.add_node("data_analyst", data_analyst_node); graph.add_node("reviewer", reviewer_node)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route_worker, {"software_engineer": "software_engineer", "data_analyst": "data_analyst"})
    graph.add_edge("software_engineer", "reviewer"); graph.add_edge("data_analyst", "reviewer")
    graph.add_conditional_edges("reviewer", route_review, {"retry": "supervisor", "done": END})
    return graph.compile()
