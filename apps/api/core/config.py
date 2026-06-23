from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'Startup Ops Workspace'
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    llm_provider: str = "offline"  # offline | deepseek | gemini
    deepseek_api_key: str | None = None
    deepseek_model: str = "deepseek-chat"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    ai_timeout_seconds: int = 45
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
