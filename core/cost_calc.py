def estimate_cost(route: str, response_length: int = 100) -> float:
    # Based on the user assumption for cost model
    cost_model = {
        "calculator": 0.0000,
        "rule_engine": 0.0000,
        "search": 0.0001,
        "local_llm": 0.0010,
        "large_llm": 0.0300
    }
    return cost_model.get(route, 0.0)
