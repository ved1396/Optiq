import requests
import logging
from engines.base import BaseEngine
from config import settings

logger = logging.getLogger(__name__)

class LocalLLMEngine(BaseEngine):
    def process(self, query: str) -> str:
        url = f"{settings.ollama_endpoint}/api/generate"
        payload = {
            "model": settings.ollama_model,
            "prompt": query,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Local LLM Error: {e}")
            return "Mock Local LLM Response: (Could not connect to Ollama. Ensure it's running locally.) \nQuery: " + query
