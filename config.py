import os
from functools import lru_cache
from typing import Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized runtime configuration for backend and dashboard clients."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Optiq AI Router API"
    app_version: str = "2.0.0"
    log_level: str = "INFO"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "sqlite:///./optiq.db"

    classifier_model_path: str = "classifier/model.joblib"
    classifier_confidence_threshold: float = 0.52

    search_api_url: str = "https://api.duckduckgo.com/"
    search_timeout_seconds: int = 8

    ollama_endpoint: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_timeout_seconds: int = 20

    openai_api_key: str = ""
    openai_api_url: str = "https://api.openai.com/v1/chat/completions"
    openai_model: str = "gpt-4o-mini"
    openai_timeout_seconds: int = 30

    baseline_large_llm_cost: float = 0.0300
    baseline_large_llm_energy: float = 120.0

    route_base_costs: Dict[str, float] = Field(
        default_factory=lambda: {
            "calculator": 0.00002,
            "rule_engine": 0.00003,
            "search": 0.00060,
            "local_llm": 0.00350,
            "large_llm": 0.03000,
        }
    )
    route_cost_per_1k_chars: Dict[str, float] = Field(
        default_factory=lambda: {
            "calculator": 0.0,
            "rule_engine": 0.0,
            "search": 0.00005,
            "local_llm": 0.00035,
            "large_llm": 0.00180,
        }
    )
    route_base_energy: Dict[str, float] = Field(
        default_factory=lambda: {
            "calculator": 0.8,
            "rule_engine": 1.2,
            "search": 6.0,
            "local_llm": 28.0,
            "large_llm": 120.0,
        }
    )
    route_energy_per_second: Dict[str, float] = Field(
        default_factory=lambda: {
            "calculator": 0.2,
            "rule_engine": 0.3,
            "search": 1.0,
            "local_llm": 5.5,
            "large_llm": 14.0,
        }
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        ollama_endpoint=os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./optiq.db"),
    )


settings = get_settings()
