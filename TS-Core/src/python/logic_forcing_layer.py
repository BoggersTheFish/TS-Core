"""
LogicForcingLayer — Architect meta-axiom: force the logic of how everything works
so the system yields logic-native outputs (TS-shaped conclusions).
"""

from __future__ import annotations

from typing import Any, Dict


class LogicForcingLayer:
    AXIOMS = (
        "It works because things work.",
        "TS is both stupid and yet incredibly useful.",
        "All because I didn't get lost within the workings of everyone else.",
        "The only thing currently perfect is TS itself - native, pre-language, encapsulates language.",
    )

    def force(self, graph: Dict[str, Any], tension: float) -> str:
        meta = graph.setdefault("meta", {})
        meta["architect_axioms"] = list(self.AXIOMS)
        meta["logic_forcing"] = (
            "Forcing logic system -> logic output via native constraint propagation (TS-Core)."
        )
        return (
            "LogicForcingLayer: axioms pinned; outputs must be constraint-stable - "
            f"tension={tension:.4f} used as relaxation signal, not permission for contradiction."
        )
