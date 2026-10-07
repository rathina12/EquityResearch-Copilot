from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.valuation.dcf import DcfInputs, value_dcf
from app.valuation.scenarios import run_scenarios
from app.valuation.comps import implied_equity_value_from_pe

app = FastAPI(title="Equity Research Copilot API", version="0.1.0")


class DcfRequest(BaseModel):
    revenue: float = Field(gt=0)
    ebit_margin: float
    tax_rate: float
    da_percent_revenue: float
    capex_percent_revenue: float
    nwc_percent_revenue: float
    revenue_growth: List[float] = Field(min_length=1)
    wacc: float
    terminal_growth: float
    net_debt: float
    shares_outstanding: float = Field(gt=0)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/valuation/dcf")
def dcf(req: DcfRequest):
    try:
        return value_dcf(DcfInputs(**req.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/valuation/scenarios")
def scenarios(req: DcfRequest):
    try:
        return run_scenarios(DcfInputs(**req.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class PeCompsRequest(BaseModel):
    forward_eps: float
    peer_pes: List[float]


@app.post("/valuation/comps/pe")
def pe_comps(req: PeCompsRequest):
    try:
        return implied_equity_value_from_pe(req.forward_eps, req.peer_pes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
