import logging
import random
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

TRAINING_DATA = {
    "calculator": [
        "what is 12 + 7",
        "calculate 98 / 7",
        "solve 4 * (8 + 2)",
        "what is the square root of 144",
        "compute 15% of 250",
        "evaluate 3^4 - 5",
    ],
    "rule_engine": [
        "hello",
        "hi there",
        "help",
        "what is optiq",
        "who created you",
        "how are you",
        "good morning",
        "what do you do",
    ],
    "search": [
        "who is the president of france",
        "latest news about ai chips",
        "what is the capital of peru",
        "when is the next solar eclipse",
        "stock price of microsoft",
        "weather in tokyo",
    ],
    "local_llm": [
        "summarize this paragraph about renewable energy",
        "rewrite this email to sound more professional",
        "translate this sentence into spanish",
        "draft a quick status update for my manager",
        "explain docker in simple terms",
        "short summary of this meeting transcript",
    ],
    "large_llm": [
        "design a distributed event-driven architecture for ecommerce",
        "compare transformers and rnns in detail",
        "write a multi-step migration plan for a monolith to microservices",
        "analyze this business strategy and identify risks",
        "generate a backend architecture for an ai platform",
        "reason through the tradeoffs of vector databases for rag",
    ],
}

FILLERS = [
    "sales forecasting",
    "customer support",
    "python automation",
    "renewable energy",
    "fintech compliance",
    "machine learning",
    "project planning",
]


def generate_dataset(samples_per_class: int = 120) -> pd.DataFrame:
    random.seed(42)
    records: list[dict[str, str]] = []
    for label, seeds in TRAINING_DATA.items():
        for _ in range(samples_per_class):
            seed = random.choice(seeds)
            filler = random.choice(FILLERS)
            variants = [
                seed,
                f"{seed} for {filler}",
                f"please {seed}",
                f"can you {seed}",
                f"{seed} today",
            ]
            records.append({"query": random.choice(variants), "label": label})
    return pd.DataFrame(records)


def train_model() -> Path:
    df = generate_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        df["query"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42)),
        ]
    )
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    logger.info("\n%s", classification_report(y_test, predictions))

    model_path = Path(__file__).with_name("model.joblib")
    joblib.dump(pipeline, model_path)
    logger.info("Saved classifier model to %s", model_path)
    return model_path


if __name__ == "__main__":
    train_model()
