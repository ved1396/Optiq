import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import random
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define basic synthetic data templates
DATA = {
    "calculator": [
        "What is {} + {}?",
        "Calculate {} * {}",
        "{} divided by {}",
        "Solve {} - {}",
        "Math: {} / {}",
        "Compute the sum of {} and {}"
    ],
    "rule_engine": [
        "Hello",
        "Hi there",
        "What is your name?",
        "How are you?",
        "Good morning",
        "Who created you?",
        "Help me",
        "FAQ"
    ],
    "search": [
        "What is the current weather in {}?",
        "Who won the {} election?",
        "Latest news about {}",
        "Stock price of {}",
        "When is the next eclipse?",
        "Who is the CEO of {}?"
    ],
    "local_llm": [
        "Summarize this text: {}",
        "Write a short email about {}",
        "Give me a brief overview of {}",
        "Translate this to French: {}",
        "Draft a message saying {}",
        "Explain {} simply"
    ],
    "large_llm": [
        "Write a complex Python script for {}",
        "Design a system architecture for {}",
        "Explain the quantum mechanics of {}",
        "Write a philosophical essay comparing {} and {}",
        "Generate a complete React application that does {}",
        "Analyze the following dataset and provide deep insights: {}"
    ]
}

FILLERS = ["Apple", "Google", "AI", "the economy", "2024", "history", "physics", "New York", "London", "10", "42"]

def generate_dataset(num_samples=600):
    records = []
    for _ in range(num_samples):
        category = random.choice(list(DATA.keys()))
        template = random.choice(DATA[category])
        
        # Fill in placeholders if any
        if "{}" in template:
            num_blanks = template.count("{}")
            fills = [str(random.choice(FILLERS)) if category != "calculator" else str(random.randint(1, 1000)) for _ in range(num_blanks)]
            query = template.format(*fills)
        else:
            query = template
            
        records.append({"query": query, "label": category})
        
    return pd.DataFrame(records)

def train_model():
    logger.info("Generating synthetic dataset...")
    df = generate_dataset(600)
    
    logger.info("Training TF-IDF + Logistic Regression model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    
    pipeline.fit(df['query'], df['label'])
    
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
