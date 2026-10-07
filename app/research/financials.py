from typing import Dict


def calculate_kpis(current: Dict[str, float], previous: Dict[str, float]) -> Dict[str, float]:
    revenue = current["revenue"]
    prev_revenue = previous["revenue"]
    ebit = current["ebit"]
    net_income = current["net_income"]
    invested_capital = current.get("invested_capital", 0)
    tax_rate = current.get("tax_rate", 0.25)
    return {
        "revenue_growth": (revenue / prev_revenue - 1) if prev_revenue else 0.0,
        "ebit_margin": ebit / revenue if revenue else 0.0,
        "net_margin": net_income / revenue if revenue else 0.0,
        "roic": (ebit * (1 - tax_rate) / invested_capital) if invested_capital else 0.0,
        "fcf_margin": current.get("free_cash_flow", 0) / revenue if revenue else 0.0,
    }
