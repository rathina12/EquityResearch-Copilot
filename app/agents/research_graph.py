from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, START, END


class ResearchState(TypedDict, total=False):
    ticker: str
    source_evidence: List[Dict]
    financial_summary: Dict
    risks: List[str]
    catalysts: List[str]
    valuation: Dict
    report_sections: Dict[str, str]
    verification_errors: List[str]


def verify_sources(state: ResearchState) -> ResearchState:
    errors = []
    for item in state.get("source_evidence", []):
        if not item.get("source_id") or not item.get("text"):
            errors.append("Evidence item missing source_id or text")
    return {"verification_errors": errors}


def build_report_outline(state: ResearchState) -> ResearchState:
    sections = {
        "investment_thesis": "Pending analyst synthesis from verified evidence",
        "financial_analysis": "Pending deterministic KPI/forecast output",
        "valuation": "Pending DCF/comps/scenario output",
        "risks": "Pending source-grounded risk synthesis",
        "catalysts": "Pending source-grounded catalyst synthesis",
    }
    return {"report_sections": sections}


def build_research_graph():
    graph = StateGraph(ResearchState)
    graph.add_node("verify_sources", verify_sources)
    graph.add_node("build_report_outline", build_report_outline)
    graph.add_edge(START, "verify_sources")
    graph.add_edge("verify_sources", "build_report_outline")
    graph.add_edge("build_report_outline", END)
    return graph.compile()
