from engines.base import BaseEngine

class RuleEngine(BaseEngine):
    def process(self, query: str) -> str:
        q = query.lower().strip()
        if any(greet in q for greet in ["hi", "hello", "hi there", "hello there", "good morning"]):
            return "Hello! I am Optiq, your intelligent AI router. How can I help you today?"
        if "how are you" in q:
            return "I'm functioning at optimal efficiency. Thanks for asking!"
        if "who created you" in q or "what are you" in q:
            return "I am Optiq, built to route your queries to the most efficient processing engine."
        
        return "I am a simple rule engine. I don't have an answer for that yet!"
