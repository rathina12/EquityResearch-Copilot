from dataclasses import replace
from typing import Dict
from .dcf import DcfInputs, value_dcf


def run_scenarios(base: DcfInputs) -> Dict[str, dict]:
    bear = replace(
        base,
        revenue_growth=[max(-0.2, g - 0.04) for g in base.revenue_growth],
        ebit_margin=max(0.0, base.ebit_margin - 0.03),
        wacc=base.wacc + 0.01,
        terminal_growth=max(0.0, base.terminal_growth - 0.005),
    )
    bull = replace(
        base,
        revenue_growth=[g + 0.04 for g in base.revenue_growth],
        ebit_margin=base.ebit_margin + 0.03,
        wacc=max(base.terminal_growth + 0.01, base.wacc - 0.01),
        terminal_growth=base.terminal_growth + 0.005,
    )
    return {
        "bear": value_dcf(bear),
        "base": value_dcf(base),
        "bull": value_dcf(bull),
    }
