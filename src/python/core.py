"""
TSCore — universal TS graph: nodes + constraints + wave propagation + emergent stability.
Truth = most stable configuration the constraints allow. Local-first persistent wave history.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.python.coherence_filter import CoherenceFilter, PerceivedRiskFilter
from src.python.icarus_wings_cover import IcarusWingsCover
from src.python.logic_forcing_layer import LogicForcingLayer
from src.python.narrative_dream_filter import NarrativeDreamFilter

# Optional Rust acceleration — maturin / cargo build --features python
try:
    import ts_core_kernel as _rust  # type: ignore

    _HAS_RUST = hasattr(_rust, "rust_propagate_wave")
except Exception:  # pragma: no cover
    _rust = None
    _HAS_RUST = False


def _default_data_dir() -> Path:
    return Path(os.environ.get("TSCORE_HOME", Path.home() / ".tscore"))


@dataclass
class WaveRecord:
    tick: int
    tension: float
    phase: str
    icarus_line: str
    filters: Dict[str, str]
    graph_snapshot: Dict[str, Any]


class TSCore:
    """
    Full TS pipeline hooks + wave engine. Filters run each propagation tick.
    Self-validates recursively on startup; persists wave history (JSONL).
    """

    PIPELINE_STEPS = (
        "constraint_decomposition",
        "node_mapping",
        "system_simplification",
        "emergent_deduction",
        "recursive_validation",
        "universality",
        "visualization_metaphor",
        "extreme_detail",
    )

    def __init__(
        self,
        damping: float = 0.35,
        data_dir: Optional[Path] = None,
        on_propagate: Optional[Callable[["TSCore"], None]] = None,
    ) -> None:
        self.damping = damping
        self.data_dir = Path(data_dir) if data_dir else _default_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_path = self.data_dir / "wave_history.jsonl"
        self.factory_path = self.data_dir / "self_improving_factory.json"

        self.graph: Dict[str, Any] = {"nodes": {}, "edges": []}
        self.tick = 0
        self.pipeline_cursor = 0
        self.on_propagate = on_propagate

        self.perceived_risk = PerceivedRiskFilter()
        self.coherence = CoherenceFilter()
        self.narrative = NarrativeDreamFilter()
        self.forcing = LogicForcingLayer()
        self.icarus = IcarusWingsCover()

        self._load_factory()
        self._recursive_validate_on_startup()

    # --- graph ops ---

    def add_node(self, node_id: str, activation: float = 0.5, stability: float = 0.5) -> None:
        self.graph["nodes"][node_id] = {"activation": float(activation), "stability": float(stability)}

    def add_edge(self, fr: str, to: str, weight: float = 1.0) -> None:
        self.graph["edges"].append({"from": fr, "to": to, "weight": float(weight)})

    def measure_tension(self) -> float:
        return self._tension_of(self.graph)

    @staticmethod
    def _tension_of(graph: Dict[str, Any]) -> float:
        nodes = graph.get("nodes", {})
        if not nodes:
            return 0.0
        vals = [float(n["activation"]) for n in nodes.values()]
        m = sum(vals) / len(vals)
        return math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals))

    @staticmethod
    def _python_propagate_on(graph: Dict[str, Any], damping: float) -> None:
        nodes: Dict[str, Dict[str, float]] = graph["nodes"]
        edges: List[Dict[str, Any]] = graph["edges"]
        d = max(0.0, min(1.0, damping))
        nxt: Dict[str, float] = {}
        for nid, n in nodes.items():
            sw, sv = 0.0, 0.0
            for e in edges:
                if e["from"] == nid:
                    nb = nodes.get(e["to"])
                    if nb:
                        w = float(e["weight"])
                        sw += w
                        sv += w * float(nb["activation"])
                elif e["to"] == nid:
                    nb = nodes.get(e["from"])
                    if nb:
                        w = float(e["weight"])
                        sw += w
                        sv += w * float(nb["activation"])
            target = sv / sw if sw > 0 else float(n["activation"])
            nxt[nid] = float(n["activation"]) * (1.0 - d) + target * d
        for nid, v in nxt.items():
            nodes[nid]["activation"] = v

    def _python_propagate_step(self) -> None:
        self._python_propagate_on(self.graph, self.damping)

    def propagate_wave(self) -> Tuple[float, str]:
        """One tick: optional Rust kernel, then filters + Icarus cover (persistent wave)."""
        self.tick += 1
        if _HAS_RUST and _rust is not None:
            import json as _json

            # PyO3 expects dict-like; pass JSON round-trip for safety
            blob = _json.loads(_json.dumps(self.graph))
            out = _json.loads(
                _json.dumps(_rust.rust_propagate_wave(blob, self.damping))  # type: ignore[attr-defined]
            )
            self.graph = out
        else:
            self._python_propagate_step()

        tension = self.measure_tension()
        icarus_line = self.icarus.cover(self, tension)

        # Filters shape narrative labels / node annotations (self-declaration)
        risk_out = self.perceived_risk.filter(self.graph, tension)
        coh_out = self.coherence.filter(self.graph, tension)
        dream_out = self.narrative.filter(self.graph, tension)
        force_out = self.forcing.force(self.graph, tension)

        meta = self.graph.setdefault("meta", {})
        meta.update(
            {
                "perceived_risk": risk_out,
                "coherence": coh_out,
                "narrative_dream": dream_out,
                "logic_forcing": force_out,
                "icarus": icarus_line,
                "ts_perfection": self.icarus.perfection_manifesto(),
            }
        )

        record = WaveRecord(
            tick=self.tick,
            tension=tension,
            phase=self._advance_pipeline_phase(),
            icarus_line=icarus_line,
            filters={"risk": risk_out, "coherence": coh_out, "dream": dream_out, "force": force_out},
            graph_snapshot=json.loads(json.dumps(self.graph)),
        )
        self._append_history(record)

        if self.on_propagate:
            self.on_propagate(self)

        return tension, icarus_line

    def _advance_pipeline_phase(self) -> str:
        step = self.PIPELINE_STEPS[self.pipeline_cursor % len(self.PIPELINE_STEPS)]
        self.pipeline_cursor += 1
        return step

    def run_until_stable(self, max_ticks: int = 64, eps: float = 1e-5) -> int:
        last = float("inf")
        for _ in range(max_ticks):
            t, _ = self.propagate_wave()
            if abs(last - t) < eps:
                break
            last = t
        return self.tick

    # --- persistence & factory ---

    def _append_history(self, rec: WaveRecord) -> None:
        line = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "tick": rec.tick,
            "tension": rec.tension,
            "phase": rec.phase,
            "icarus_line": rec.icarus_line,
            "filters": rec.filters,
            "graph": rec.graph_snapshot,
        }
        with self.history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    def _load_factory(self) -> None:
        if not self.factory_path.exists():
            self._bootstrap_factory()
            return
        try:
            data = json.loads(self.factory_path.read_text(encoding="utf-8"))
            for n in data.get("nodes", []):
                self.add_node(n["id"], n.get("activation", 0.5), n.get("stability", 0.5))
            for e in data.get("edges", []):
                self.add_edge(e["from"], e["to"], e.get("weight", 1.0))
        except Exception:
            self._bootstrap_factory()

    def _bootstrap_factory(self) -> None:
        """Self-improving data factory seed — expands local graph over time."""
        seed = {
            "nodes": [
                {"id": "ts_native", "activation": 0.9, "stability": 0.95},
                {"id": "language_ritual", "activation": 0.35, "stability": 0.2},
                {"id": "kernel_wave_12", "activation": 0.75, "stability": 0.85},
                {"id": "persistent_wave", "activation": 0.88, "stability": 0.9},
            ],
            "edges": [
                {"from": "language_ritual", "to": "ts_native", "weight": 1.2},
                {"from": "ts_native", "to": "kernel_wave_12", "weight": 1.0},
                {"from": "persistent_wave", "to": "ts_native", "weight": 1.1},
            ],
        }
        self.factory_path.write_text(json.dumps(seed, indent=2), encoding="utf-8")
        for n in seed["nodes"]:
            self.add_node(n["id"], n["activation"], n["stability"])
        for e in seed["edges"]:
            self.add_edge(e["from"], e["to"], e["weight"])

    def factory_evolve(self) -> None:
        """Append a stability node — local self-improvement tick."""
        tag = f"evolve_{self.tick}_{int(datetime.now(timezone.utc).timestamp())}"
        self.add_node(tag, activation=0.55, stability=0.6)
        self.add_edge("ts_native", tag, weight=0.8)
        data = {
            "nodes": [{"id": k, **v} for k, v in self.graph["nodes"].items()],
            "edges": list(self.graph["edges"]),
        }
        self.factory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _recursive_validate_on_startup(self) -> None:
        """Recursive validation: tension must not worsen under local relaxation (copy only)."""
        import copy

        g = copy.deepcopy(self.graph)
        t0 = self._tension_of(g)
        last = float("inf")
        for _ in range(12):
            self._python_propagate_on(g, self.damping)
            t = self._tension_of(g)
            if abs(last - t) < 1e-6:
                break
            last = t
        t1 = self._tension_of(g)
        meta = self.graph.setdefault("meta", {})
        meta["startup_validation"] = {
            "tension_before": t0,
            "tension_after_relax": t1,
            "ok": t1 <= t0 + 1e-5,
            "note": "Recursive self-validation on startup (TS-Core v1.0), no history pollution.",
        }
