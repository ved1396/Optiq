import argparse
import logging
from pathlib import Path
from typing import Tuple

import joblib

from config import settings

logger = logging.getLogger(__name__)


class IntentClassifier:
    def __init__(self, model_path: str | None = None):
        resolved_path = model_path or settings.classifier_model_path
        self.model_path = Path(resolved_path)
        self.model = None
        self.load_model()

    def load_model(self) -> None:
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
            logger.info("Loaded classifier from %s", self.model_path)
        else:
            logger.warning("Classifier model not found at %s", self.model_path)

    def predict(self, query: str) -> Tuple[str, float]:
        if self.model is None:
            return "large_llm", 0.0
        probabilities = self.model.predict_proba([query])[0]
        top_index = probabilities.argmax()
        return self.model.classes_[top_index], float(probabilities[top_index])

    def predict_with_scores(self, query: str) -> dict[str, float]:
        if self.model is None:
            return {"large_llm": 0.0}
        probabilities = self.model.predict_proba([query])[0]
        return {
            label: round(float(probability), 4)
            for label, probability in zip(self.model.classes_, probabilities, strict=False)
        }


classifier = IntentClassifier()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Optiq intent classification inference.")
    parser.add_argument("query", help="The input query to classify")
    args = parser.parse_args()

    label, confidence = classifier.predict(args.query)
    print({"route": label, "confidence": round(confidence, 4), "scores": classifier.predict_with_scores(args.query)})
