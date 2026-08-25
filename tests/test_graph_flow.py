from src.graph import build_graph

def test_end_to_end_software_flow():
    result = build_graph().invoke({"messages": [{"role": "user", "content": "Build a Python API"}]})
    assert result["status"] == "completed"
    assert result["active_worker"] == "software_engineer"

def test_end_to_end_data_flow():
    result = build_graph().invoke({"messages": [{"role": "user", "content": "Analyze this CSV dataset"}]})
    assert result["status"] == "completed"
    assert result["active_worker"] == "data_analyst"
