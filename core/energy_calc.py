from config import settings


def estimate_energy(route: str, latency_ms: float) -> float:
    base_energy = settings.route_base_energy.get(route, settings.baseline_large_llm_energy)
    variable_energy = settings.route_energy_per_second.get(route, 0.0) * (latency_ms / 1000)
    return round(base_energy + variable_energy, 3)


def estimate_energy_saved(route: str, estimated_energy: float) -> float:
    baseline = settings.route_base_energy.get("large_llm", settings.baseline_large_llm_energy)
    if route == "large_llm":
        return 0.0
    return round(max(baseline - estimated_energy, 0.0), 3)
