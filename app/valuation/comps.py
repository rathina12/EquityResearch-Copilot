from statistics import median
from typing import Iterable, Dict


def implied_equity_value_from_pe(forward_eps: float, peer_pes: Iterable[float]) -> Dict[str, float]:
    peers = [x for x in peer_pes if x > 0]
    if not peers:
        raise ValueError("At least one positive peer P/E is required")
    peer_median = median(peers)
    return {"peer_median_pe": peer_median, "implied_price": forward_eps * peer_median}


def implied_ev_from_ebitda(forward_ebitda: float, peer_ev_ebitda: Iterable[float]) -> Dict[str, float]:
    peers = [x for x in peer_ev_ebitda if x > 0]
    if not peers:
        raise ValueError("At least one positive EV/EBITDA multiple is required")
    peer_median = median(peers)
    return {"peer_median_ev_ebitda": peer_median, "implied_enterprise_value": forward_ebitda * peer_median}
