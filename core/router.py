import logging
import re
import time

from classifier.inference import classifier
from config import settings
from core.analytics_logger import log_query
from core.cost_calc import estimate_cost
from core.energy_calc import estimate_energy
from engines.calculator import CalculatorEngine
from engines.large_llm import LargeLLMEngine
from engines.local_llm import LocalLLMEngine
from engines.rule_engine import RuleEngine
from engines.search_wrapper import SearchEngine

logger = logging.getLogger(__name__)

ENGINES = {
    "calculator": CalculatorEngine(),
    "rule_engine": RuleEngine(),
    "search": SearchEngine(),
    "local_llm": LocalLLMEngine(),
    "large_llm": LargeLLMEngine(),
}

MATH_PATTERN = re.compile(r"(\d+\s*[\+\-\*\/\%\^]\s*\d+)|calculate|solve|compute|evaluate", re.IGNORECASE)
GREETING_PATTERN = re.compile(r"\b(hi|hello|hey|good morning|good evening|help|faq)\b", re.IGNORECASE)
FAQ_PATTERN = re.compile(r"\b(who created you|what is optiq|what do you do|how are you)\b", re.IGNORECASE)
SEARCH_PATTERN = re.compile(
    r"\b(who is|what is the capital|latest|current|today|weather|stock price|news|when is|facts about)\b",
    re.IGNORECASE,
)
LOCAL_TASK_PATTERN = re.compile(
    r"\b(summarize|rewrite|translate|paraphrase|short email|brief overview|simple explanation|draft)\b",
    re.IGNORECASE,
)
COMPLEX_PATTERN = re.compile(
    r"\b(design|architecture|analyze|compare|tradeoffs|strategy|plan|debug|reason|generate a complete)\b",
    re.IGNORECASE,
)


def detect_route(query: str) -> str | None:
    normalized = query.strip()
    if not normalized:
        return "rule_engine"
    if MATH_PATTERN.search(normalized):
        return "calculator"
    if GREETING_PATTERN.search(normalized) or FAQ_PATTERN.search(normalized):
        return "rule_engine"
    if SEARCH_PATTERN.search(normalized):
        return "search"
    if LOCAL_TASK_PATTERN.search(normalized):
        return "local_llm"
    if COMPLEX_PATTERN.search(normalized):
        return "large_llm"
    return None


def process_and_route(query: str) -> dict:
    started_at = time.perf_counter()
    heuristic_route = detect_route(query)
    classifier_label, confidence = classifier.predict(query)

    if heuristic_route:
        selected_route = heuristic_route
    elif confidence >= settings.classifier_confidence_threshold:
        selected_route = classifier_label
    else:
        selected_route = "large_llm"

    engine = ENGINES.get(selected_route, ENGINES["large_llm"])
    try:
        response = engine.process(query)
    except Exception as exc:
        logger.exception("Engine failure for route %s", selected_route)
        selected_route = "large_llm"
        response = f"Optiq encountered an internal routing error: {exc}"

    latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
    estimated_cost = estimate_cost(selected_route, query, response)
    estimated_energy = estimate_energy(selected_route, latency_ms)
    query_id = log_query(
        query=query,
        route=selected_route,
        response=response,
        latency_ms=latency_ms,
        estimated_cost=estimated_cost,
        estimated_energy=estimated_energy,
        confidence_score=confidence,
        classifier_label=classifier_label,
        heuristic_route=heuristic_route,
    )

    return {
        "query_id": query_id,
        "query": query,
        "route": selected_route,
        "response": response,
        "confidence_score": round(confidence, 4),
        "classifier_label": classifier_label,
        "heuristic_route": heuristic_route,
        "latency_ms": latency_ms,
        "estimated_cost": estimated_cost,
        "estimated_energy": estimated_energy,
    }
