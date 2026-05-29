import logging

import requests

from config import settings
from engines.base import BaseEngine

logger = logging.getLogger(__name__)


class LargeLLMEngine(BaseEngine):
    """Wrapper for a hosted large-model completion endpoint."""

    def process(self, query: str) -> str:
        if not settings.openai_api_key:
            return (
                "Large LLM fallback response: no external API key is configured, "
                "so this complex task is being simulated locally."
            )

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.openai_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a precise assistant for complex reasoning and code generation tasks.",
                },
                {"role": "user", "content": query},
            ],
            "temperature": 0.2,
        }
        try:
            response = requests.post(
                settings.openai_api_url,
                headers=headers,
                json=payload,
                timeout=settings.openai_timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as exc:
            logger.error("Large LLM request failed: %s", exc)
            return "Large LLM request failed, so Optiq returned a safe fallback response instead."
