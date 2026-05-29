from abc import ABC, abstractmethod

class BaseEngine(ABC):
    @abstractmethod
    def process(self, query: str) -> str:
        """Processes the query and returns a response string."""
        pass
