import pytest

from src.config import get_settings


@pytest.fixture(autouse=True)
def isolated_workspace(tmp_path, monkeypatch):
    """Point WORKSPACE_ROOT at a temp dir and reset the cached settings for every test."""
    monkeypatch.setenv("WORKSPACE_ROOT", str(tmp_path / "workspace"))
    get_settings.cache_clear()
    yield tmp_path / "workspace"
    get_settings.cache_clear()
