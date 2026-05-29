def currency(value: float) -> str:
    return f"${value:,.4f}"


def energy(value: float) -> str:
    return f"{value:,.2f} Wh"


def latency(value: float) -> str:
    return f"{value:,.2f} ms"
