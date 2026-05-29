import requests
import logging
from engines.base import BaseEngine
from config import settings

logger = logging.getLogger(__name__)

class LargeLLMEngine(BaseEngine):
    def process(self, query: str) -> str:
        if not settings.openai_api_key:
            logger.warning("No OPENAI_API_KEY provided. Using simulated response.")
            return f"Mock Large LLM Response for: '{query}' (Add an API key to enable actual calls)"

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4-turbo",  # default to a generic model
            "messages": [{"role": "user", "content": query}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Large LLM Error: {e}")
            return f"Error communicating with external API: {str(e)}"
