from engines.base import BaseEngine

class SearchEngine(BaseEngine):
    def process(self, query: str) -> str:
        # Simulated search for MVP
        return f"Mock search result for '{query}': According to the latest available data, the answer is 42."
