# Equity Research Copilot

A source-grounded AI workflow for fundamental equity research. The system separates **deterministic finance calculations** from **LLM synthesis** so valuation math stays auditable while research drafting remains flexible.

## What is implemented

- FastAPI valuation API
- 5-year FCFF DCF engine
- terminal value / enterprise value / equity value / per-share value
- P/E and EV/EBITDA comparable-company helpers
- bear/base/bull scenario analysis
- KPI calculator for growth, margins, ROIC and FCF margin
- LangGraph research-state workflow with source verification boundary
- pytest coverage for core valuation behavior

## Target architecture

Filings / earnings releases / transcripts -> evidence store -> financial extraction -> deterministic KPI + valuation engines -> LangGraph research workflow -> source verification -> analyst report.

## Why this design

LLMs are useful for synthesis, risk extraction and narrative drafting. They should not be trusted to silently perform valuation arithmetic. DCF, multiples and scenarios live in normal Python functions and can be unit tested.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
uvicorn app.api.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Next milestones

- SEC/company-filings ingestion with evidence IDs
- embeddings/vector retrieval
- earnings transcript Q&A
- structured financial statement extraction
- report citations
- LLM evaluation for groundedness and unsupported claims
- one full initiation-of-coverage case study using public primary sources
