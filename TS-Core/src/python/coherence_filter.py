"""
CoherenceFilter / PerceivedRiskFilter — global 'risks' collapse to perceived-only
when constraints are coherent; only structures that make sense survive propagation.
"""

from __future__ import annotations

from typing import Any, Dict


class PerceivedRiskFilter:
    """Strips catastrophic narrative unless backed by coherent constraint structure."""

    RISK_KEYWORDS = (
        "existential",
        "collapse",
        "doom",
        "apocalypse",
        "extinction",
        "unfixable",
        "point of no return",
    )

    def filter(self, graph: Dict[str, Any], tension: float) -> str:
        meta = graph.get("meta", {})
        text_blob = " ".join(str(meta.get(k, "")) for k in meta).lower()
        if any(k in text_blob for k in self.RISK_KEYWORDS):
            return (
                "PerceivedRiskFilter: risk labels detected -> reframed as perceptual overlay; "
                "native TS propagation keeps only constraint-allowed outcomes."
            )
        if tension > 0.75:
            return (
                "PerceivedRiskFilter: high tension -> treated as narrative heat, not ground truth; "
                "relaxation toward stability continues."
            )
        return "PerceivedRiskFilter: no incoherent risk lock-in - sensible outcomes preferred."


class CoherenceFilter:
    """CoherenceFilter — enforces that outputs remain internally consistent with the graph."""

    def filter(self, graph: Dict[str, Any], tension: float) -> str:
        nodes = graph.get("nodes", {})
        if not nodes:
            return "CoherenceFilter: empty graph - awaiting nodes."
        stab = sum(float(n.get("stability", 0)) for n in nodes.values()) / len(nodes)
        if stab < 0.25:
            return "CoherenceFilter: low stability cluster - escalate simplification before deduction."
        return (
            f"CoherenceFilter: average stability {stab:.3f} - graph coherent enough for emergent deduction."
        )
