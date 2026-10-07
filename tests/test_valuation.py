import pytest
from app.valuation.dcf import DcfInputs, value_dcf
from app.valuation.scenarios import run_scenarios
from app.valuation.comps import implied_equity_value_from_pe


def fixture():
    return DcfInputs(
        revenue=1000,
        ebit_margin=0.20,
        tax_rate=0.25,
        da_percent_revenue=0.04,
        capex_percent_revenue=0.05,
        nwc_percent_revenue=0.10,
        revenue_growth=[0.10, 0.09, 0.08, 0.07, 0.06],
        wacc=0.10,
        terminal_growth=0.03,
        net_debt=100,
        shares_outstanding=100,
    )


def test_dcf_returns_positive_value_per_share():
    result = value_dcf(fixture())
    assert result["value_per_share"] > 0
    assert len(result["forecast"]) == 5


def test_invalid_terminal_growth_rejected():
    x = fixture()
    bad = DcfInputs(**{**x.__dict__, "wacc": 0.03, "terminal_growth": 0.03})
    with pytest.raises(ValueError):
        value_dcf(bad)


def test_bull_base_bear_ordering():
    scenarios = run_scenarios(fixture())
    assert scenarios["bear"]["value_per_share"] < scenarios["base"]["value_per_share"]
    assert scenarios["base"]["value_per_share"] < scenarios["bull"]["value_per_share"]


def test_pe_comps():
    result = implied_equity_value_from_pe(5.0, [20, 24, 22])
    assert result["peer_median_pe"] == 22
    assert result["implied_price"] == 110


def test_pe_comps_rejects_non_positive_peers():
    with pytest.raises(ValueError):
        implied_equity_value_from_pe(5.0, [0, -2, -10])


def test_pe_comps_ignores_invalid_peers_when_valid_values_exist():
    result = implied_equity_value_from_pe(4.0, [-5, 18, 22, 0])
    assert result["peer_median_pe"] == 20
    assert result["implied_price"] == 80
