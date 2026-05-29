import logging

import requests

from config import settings
from engines.base import BaseEngine

logger = logging.getLogger(__name__)


class LocalLLMEngine(BaseEngine):
    """Wrapper for a local Ollama-style model endpoint."""

    def process(self, query: str) -> str:
        payload = {"model": settings.ollama_model, "prompt": query, "stream": False}
        try:
            response = requests.post(
                f"{settings.ollama_endpoint}/api/generate",
                json=payload,
                timeout=settings.ollama_timeout_seconds,
            )
            response.raise_for_status()
            return response.json().get("response", "").strip() or "Local model returned an empty response."
        except requests.RequestException as exc:
            logger.warning("Local model unavailable: %s", exc)
            return (
                "Local LLM fallback response: the local model endpoint could not be reached, "
                "but this query was classified as a good fit for lightweight generation or summarization."
            )
