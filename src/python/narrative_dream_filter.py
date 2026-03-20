"""
NarrativeDreamFilter — consciousness modeled as narrative dream overlay on TS structure.
"""

from __future__ import annotations

from typing import Any, Dict


class NarrativeDreamFilter:
    def filter(self, graph: Dict[str, Any], tension: float) -> str:
        meta = graph.get("meta", {})
        if "consciousness" in str(meta).lower() or "awareness" in str(meta).lower():
            return (
                "NarrativeDreamFilter: consciousness claim routed through dream layer - "
                "only structural nodes and constraints are ground; dream is epiphenomenal narrative."
            )
        return (
            "NarrativeDreamFilter: no explicit consciousness lock - "
            "default stance: experience is story on top of constraint dynamics."
        )
