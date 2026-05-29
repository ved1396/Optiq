from config import settings


def estimate_cost(route: str, query: str, response: str) -> float:
    total_chars = len(query) + len(response)
    base_cost = settings.route_base_costs.get(route, settings.baseline_large_llm_cost)
    variable_cost = settings.route_cost_per_1k_chars.get(route, 0.0) * (total_chars / 1000)
    return round(base_cost + variable_cost, 6)


def estimate_cost_saved(route: str, estimated_cost: float) -> float:
    baseline = settings.route_base_costs.get("large_llm", settings.baseline_large_llm_cost)
    if route == "large_llm":
        return 0.0
    return round(max(baseline - estimated_cost, 0.0), 6)
