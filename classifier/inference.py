import joblib
import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class IntentClassifier:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            logger.info("Intent classifier model loaded.")
        else:
            logger.warning("Model not found. Please run train.py first.")

    def predict(self, query: str) -> Tuple[str, float]:
        if not self.model:
            # Fallback if model doesn't exist
            return "large_llm", 0.0
            
        probs = self.model.predict_proba([query])[0]
        max_prob_index = probs.argmax()
        confidence = probs[max_prob_index]
        intent = self.model.classes_[max_prob_index]
        
        return intent, confidence

# Singleton instance
classifier = IntentClassifier()
