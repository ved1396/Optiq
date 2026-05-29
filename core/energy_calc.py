def estimate_energy(route: str, latency_ms: float = 0.0) -> float:
    # Based on the user assumption for energy model
    energy_model = {
        "calculator": 1.0,
        "rule_engine": 1.0,
        "search": 5.0,
        "local_llm": 30.0,
        "large_llm": 100.0
    }
    return energy_model.get(route, 1.0)
