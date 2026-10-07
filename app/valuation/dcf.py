from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class DcfInputs:
    revenue: float
    ebit_margin: float
    tax_rate: float
    da_percent_revenue: float
    capex_percent_revenue: float
    nwc_percent_revenue: float
    revenue_growth: List[float]
    wacc: float
    terminal_growth: float
    net_debt: float
    shares_outstanding: float


def project_fcff(inputs: DcfInputs) -> List[Dict[str, float]]:
    revenue = inputs.revenue
    previous_revenue = revenue
    rows: List[Dict[str, float]] = []
    for year, growth in enumerate(inputs.revenue_growth, start=1):
        revenue *= 1 + growth
        ebit = revenue * inputs.ebit_margin
        nopat = ebit * (1 - inputs.tax_rate)
        da = revenue * inputs.da_percent_revenue
        capex = revenue * inputs.capex_percent_revenue
        nwc = revenue * inputs.nwc_percent_revenue
        prev_nwc = previous_revenue * inputs.nwc_percent_revenue
        delta_nwc = nwc - prev_nwc
        fcff = nopat + da - capex - delta_nwc
        rows.append({
            "year": year,
            "revenue": revenue,
            "ebit": ebit,
            "nopat": nopat,
            "da": da,
            "capex": capex,
            "delta_nwc": delta_nwc,
            "fcff": fcff,
        })
        previous_revenue = revenue
    return rows


def value_dcf(inputs: DcfInputs) -> Dict[str, float | list]:
    if inputs.wacc <= inputs.terminal_growth:
        raise ValueError("WACC must be greater than terminal growth")
    if inputs.shares_outstanding <= 0:
        raise ValueError("shares_outstanding must be positive")

    rows = project_fcff(inputs)
    pv_fcff = 0.0
    for row in rows:
        row["discount_factor"] = 1 / ((1 + inputs.wacc) ** row["year"])
        row["pv_fcff"] = row["fcff"] * row["discount_factor"]
        pv_fcff += row["pv_fcff"]

    terminal_fcff = rows[-1]["fcff"] * (1 + inputs.terminal_growth)
    terminal_value = terminal_fcff / (inputs.wacc - inputs.terminal_growth)
    pv_terminal = terminal_value / ((1 + inputs.wacc) ** len(rows))
    enterprise_value = pv_fcff + pv_terminal
    equity_value = enterprise_value - inputs.net_debt
    value_per_share = equity_value / inputs.shares_outstanding

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal,
        "pv_explicit_fcff": pv_fcff,
        "forecast": rows,
    }
