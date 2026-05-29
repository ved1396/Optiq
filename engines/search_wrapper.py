import logging

import requests

from config import settings
from engines.base import BaseEngine

logger = logging.getLogger(__name__)


class SearchEngine(BaseEngine):
    """Thin external search wrapper with a graceful offline fallback."""

    def process(self, query: str) -> str:
        try:
            response = requests.get(
                settings.search_api_url,
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                timeout=settings.search_timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
            abstract = payload.get("AbstractText") or payload.get("Answer")
            if abstract:
                return abstract
            related_topics = payload.get("RelatedTopics") or []
            for topic in related_topics:
                if isinstance(topic, dict) and topic.get("Text"):
                    return topic["Text"]
        except requests.RequestException as exc:
            logger.warning("Search provider unavailable: %s", exc)
        return (
            "Search provider is unavailable right now, so this is a fallback response. "
            f"The query was routed correctly as a factual search: '{query}'."
        )
