"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Validated runtime settings."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    ai_model: str = "gpt-4o-mini"
    ai_temperature: float = 0.0
    workspace_root: Path = Path("./workspace")
    max_code_seconds: int = 10
    max_review_loops: int = 2
    rag_persist_directory: Path = Path("./.chroma")

@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings singleton."""
    return Settings()
