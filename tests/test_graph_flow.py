from src.agents.reviewer import reviewer_node
from src.agents.supervisor import supervisor_node
from src.graph import build_graph, route_review


def test_end_to_end_software_flow():
    result = build_graph().invoke({"messages": [{"role": "user", "content": "Build a Python API"}]})
    assert result["status"] == "completed"
    assert result["active_worker"] == "software_engineer"
    assert result["final_answer"] == "Prepared an implementation plan for: Build a Python API"


def test_end_to_end_data_flow():
    result = build_graph().invoke({"messages": [{"role": "user", "content": "Analyze this CSV dataset"}]})
    assert result["status"] == "completed"
    assert result["active_worker"] == "data_analyst"
    assert result["artifacts"][-1]["type"] == "data_analysis"


def test_supervisor_uses_latest_user_message():
    state = supervisor_node(
        {
            "messages": [
                {"role": "user", "content": "analyze statistics"},
                {"role": "assistant", "content": "ok"},
                {"role": "user", "content": "now write a function"},
            ]
        }
    )
    assert state["task"] == "now write a function"
    assert state["active_worker"] == "software_engineer"


def test_reviewer_requests_retry_without_artifact():
    state = reviewer_node({"artifacts": [], "review_loops": 0})
    assert state["status"] == "failed"
    assert state["review_loops"] == 1
    assert route_review(state) == "retry"


def test_review_loop_is_bounded_by_settings(monkeypatch):
    from src.config import get_settings

    monkeypatch.setenv("MAX_REVIEW_LOOPS", "3")
    get_settings.cache_clear()
    assert route_review({"status": "failed", "review_loops": 2}) == "retry"
    assert route_review({"status": "failed", "review_loops": 3}) == "done"
    assert route_review({"status": "completed"}) == "done"
