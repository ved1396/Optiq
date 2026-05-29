import time
import logging
from classifier.inference import classifier
from core.cost_calc import estimate_cost
from core.energy_calc import estimate_energy
from db.database import get_db_connection

# Engines
from engines.calculator import CalculatorEngine
from engines.rule_engine import RuleEngine
from engines.search_wrapper import SearchEngine
from engines.local_llm import LocalLLMEngine
from engines.large_llm import LargeLLMEngine

logger = logging.getLogger(__name__)

engines = {
    "calculator": CalculatorEngine(),
    "rule_engine": RuleEngine(),
    "search": SearchEngine(),
    "local_llm": LocalLLMEngine(),
    "large_llm": LargeLLMEngine()
}

def process_and_route(query: str):
    start_time = time.time()
    
    # 1. Classify Intent
    route, confidence = classifier.predict(query)
    
    # Fallback to safe route if engine not found
    if route not in engines:
        logger.warning(f"Unknown route '{route}', defaulting to 'large_llm'")
        route = "large_llm"
        
    engine = engines[route]
    
    # 2. Process with the selected engine
    try:
        response = engine.process(query)
    except Exception as e:
        logger.error(f"Error in engine '{route}': {e}")
        response = f"An error occurred while processing your request: {str(e)}"
        
    latency_ms = (time.time() - start_time) * 1000.0
    
    # 3. Estimate cost and energy
    cost = estimate_cost(route, len(response))
    energy = estimate_energy(route, latency_ms)
    
    # 4. Log to database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO queries (query, route, response, latency_ms, estimated_cost, estimated_energy, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (query, route, response, latency_ms, cost, energy, confidence))
    query_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "query_id": query_id,
        "query": query,
        "route": route,
        "response": response,
        "confidence_score": confidence,
        "latency_ms": latency_ms,
        "estimated_cost": cost,
        "estimated_energy": energy
    }
