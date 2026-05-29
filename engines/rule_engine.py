from engines.base import BaseEngine


class RuleEngine(BaseEngine):
    """Handles greetings, FAQs, and lightweight support prompts."""

    FAQ_RESPONSES = {
        "what is optiq": "Optiq is an intelligent query router that chooses the most efficient engine for each request.",
        "what do you do": "I route each query to the lowest-cost engine that can still handle the task well.",
        "who created you": "Optiq is designed as a multi-engine routing system for efficient AI orchestration.",
        "help": "Try a math problem, factual search, a summary task, or a complex reasoning prompt to see the router adapt.",
    }

    def process(self, query: str) -> str:
        normalized = query.lower().strip()
        if any(greeting in normalized for greeting in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "Hello! I’m Optiq. Share a task and I’ll route it to the best engine."
        if "how are you" in normalized:
            return "I’m operating smoothly and ready to route your next query."
        for key, value in self.FAQ_RESPONSES.items():
            if key in normalized:
                return value
        return "This looks like a lightweight FAQ-style request, but I do not have a specific canned answer for it yet."
