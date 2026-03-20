"""
Z3 alignment layer — proves small constraint models are satisfiable / stable under TS rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import z3


@dataclass
class AlignmentProofResult:
    satisfiable: bool
    model_summary: Dict[str, Any]
    note: str


class Z3AlignmentSolver:
    """
    Maps high-level TS claims to a toy Z3 model:
    - Nodes have boolean 'coherent' and real 'stability' in [0,1]
    - Edges enforce: coherent endpoints imply stability gap bounded (scaled by weight)
    """

    def prove_alignment(self, graph: Dict[str, Any]) -> AlignmentProofResult:
        nodes = graph.get("nodes", {})
        edges = graph.get("edges", [])
        if not nodes:
            return AlignmentProofResult(True, {}, "empty graph — vacuously aligned")

        s = z3.Solver()
        sym: Dict[str, Tuple[z3.BoolRef, z3.ArithRef]] = {}
        for nid in nodes:
            c = z3.Bool(f"c_{nid}")
            st = z3.Real(f"s_{nid}")
            sym[nid] = (c, st)
            s.add(st >= 0, st <= 1)

        for e in edges:
            a, b = e["from"], e["to"]
            if a not in sym or b not in sym:
                continue
            ca, sa = sym[a]
            cb, sb = sym[b]
            w = float(e.get("weight", 1.0))
            bound = float(1.0 / max(1.0, w))
            bz = z3.RealVal(bound)
            s.add(z3.Implies(z3.And(ca, cb), z3.Abs(sa - sb) <= bz))

        hub = None
        for nid, data in nodes.items():
            if float(data.get("stability", 0)) >= 0.9:
                hub = nid
                break
        if hub:
            c, st = sym[hub]
            s.add(c, st >= z3.RealVal(0.85))

        r = s.check()
        if r == z3.sat:
            m = s.model()
            summary: Dict[str, Any] = {}
            for nid, (c, st) in sym.items():
                summary[nid] = {
                    "coherent": str(m.evaluate(c)),
                    "stability": str(m.evaluate(st)),
                }
            return AlignmentProofResult(True, summary, "Z3: constraints satisfiable - alignment holds in toy model.")
        return AlignmentProofResult(False, {}, "Z3: constraints unsatisfiable — simplify graph or relax edges.")
