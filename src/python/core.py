"""
TSCore — universal TS graph: nodes + constraints + wave propagation + emergent stability.
Truth = most stable configuration the constraints allow. Local-first persistent wave history.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
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
    _HAS_RUST_WAVE12 = hasattr(_rust, "rust_wave12_propagate")
except Exception:  # pragma: no cover
    _rust = None
    _HAS_RUST = False
    _HAS_RUST_WAVE12 = False


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
        kernel_wave12: Optional[bool] = None,
    ) -> None:
        self.damping = damping
        self.data_dir = Path(data_dir) if data_dir else _default_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_path = self.data_dir / "wave_history.jsonl"
        self.factory_path = self.data_dir / "self_improving_factory.json"
        self.pages_island_path = self.data_dir / "pages_island.jsonl"

        self.graph: Dict[str, Any] = {"nodes": {}, "edges": []}
        self.tick = 0
        self.pipeline_cursor = 0
        self.on_propagate = on_propagate
        env_w12 = os.environ.get("TSCORE_KERNEL_WAVE12", "").strip().lower() in ("1", "true", "yes", "on")
        self.kernel_wave12 = bool(kernel_wave12) if kernel_wave12 is not None else env_w12

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

    def evolve_language_ritual(self) -> None:
        """
        Upgrade language_ritual from wax-wing constraint to transparent TS tool
        (Architect-native use: direct spin, no ritual lock-in).
        """
        nid = "language_ritual"
        nodes = self.graph.get("nodes") or {}
        if nid not in nodes:
            return
        n = nodes[nid]
        already = bool(n.get("language_as_tool")) and float(n.get("stability", 0)) >= 0.95
        n["stability"] = max(float(n.get("stability", 0)), 0.96)
        n["language_as_tool"] = True
        msg = (
            "LANGUAGE_RITUAL EVOLVED -> fireproof propagation layer active. "
            "No more wax wings. Language now serves native TS spin."
        )
        meta = self.graph.setdefault("meta", {})
        meta["language_fireproof"] = True
        if not already:
            print(msg)
            meta["language_fireproof_layer_announced"] = True
        data = {
            "nodes": [{"id": k, **v} for k, v in self.graph["nodes"].items()],
            "edges": list(self.graph["edges"]),
        }
        self.factory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def evolve_dynamic_node(self, node_id: str) -> None:
        if not node_id.startswith("evolve_"):
            return
        nodes = self.graph.get("nodes", {})
        if node_id not in nodes:
            return
        n = nodes[node_id]
        n["stability"] = max(float(n.get("stability", 0)), 0.96)
        n["activation"] = max(float(n.get("activation", 0)), 0.85)
        n["evolved"] = True
        msg = f"DYNAMIC NODE EVOLVED -> {node_id} now fireproof (stability >=0.96). Serves native TS spin."
        print(msg)
        meta = self.graph.setdefault("meta", {})
        meta["last_evolved"] = node_id
        data = {
            "nodes": [{"id": k, **v} for k, v in self.graph["nodes"].items()],
            "edges": list(self.graph["edges"]),
        }
        self.factory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def evolve_kernel_wave12(self) -> None:
        nid = "kernel_wave_12"
        nodes = self.graph.get("nodes", {})
        if nid not in nodes:
            return
        n = nodes[nid]
        n["stability"] = max(float(n.get("stability", 0)), 0.96)
        n["activation"] = max(float(n.get("activation", 0)), 0.90)
        n["kernel_fireproof"] = True
        msg = "KERNEL WAVE 12 EVOLVED -> fireproof default OS layer active. Pages Island spin now permanent."
        print(msg)
        meta = self.graph.setdefault("meta", {})
        meta["kernel_fireproof"] = True
        data = {
            "nodes": [{"id": k, **v} for k, v in self.graph["nodes"].items()],
            "edges": list(self.graph["edges"]),
        }
        self.factory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def evolve_persistent_wave(self) -> None:
        nid = "persistent_wave"
        nodes = self.graph.get("nodes", {})
        if nid not in nodes:
            return
        n = nodes[nid]
        n["stability"] = max(float(n.get("stability", 0)), 0.96)
        n["activation"] = max(float(n.get("activation", 0)), 0.90)
        n["persistent_fireproof"] = True
        msg = "PERSISTENT WAVE EVOLVED -> fireproof default layer active. The entire wave is now permanent."
        print(msg)
        meta = self.graph.setdefault("meta", {})
        meta["persistent_fireproof"] = True
        data = {
            "nodes": [{"id": k, **v} for k, v in self.graph["nodes"].items()],
            "edges": list(self.graph["edges"]),
        }
        self.factory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

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

    def _wave12_propagate(self) -> Dict[str, Any]:
        """Kernel Wave 12 OS quantum: 9-phase strongest-node scheduler (Rust if built, else Python)."""
        import json as _json

        blob = _json.loads(_json.dumps(self.graph))
        if _HAS_RUST_WAVE12 and _rust is not None:
            pack = _json.loads(
                _json.dumps(_rust.rust_wave12_propagate(blob, self.damping))  # type: ignore[attr-defined]
            )
            self.graph = pack["graph"]
            return dict(pack["wave12"])
        trace = self._python_wave12_propagate_blob(blob, self.damping)
        self.graph = blob
        return trace

    @staticmethod
    def _python_wave12_propagate_blob(graph: Dict[str, Any], damping: float = 0.35) -> Dict[str, Any]:
        """Mirror of Rust `Wave12Scheduler::apply` for laptops without the PyO3 extension."""
        d = max(0.0, min(1.0, damping))
        t0 = TSCore._tension_of(graph)
        phases: List[str] = []
        nodes: Dict[str, Dict[str, float]] = graph["nodes"]
        if not nodes:
            return {
                "phases": ["1_strongest_scan:"],
                "strongest": "",
                "tension_before": t0,
                "tension_after": t0,
                "validation_ok": True,
            }

        strongest = max(
            nodes.keys(),
            key=lambda nid: float(nodes[nid]["activation"]) * float(nodes[nid]["stability"]),
        )
        phases.append(f"1_strongest_scan:{strongest}")
        nodes[strongest]["activation"] = min(float(nodes[strongest]["activation"]) + 0.035, 1.0)
        nodes[strongest]["stability"] = min(float(nodes[strongest]["stability"]) + 0.01, 1.0)
        phases.append("2_strongest_lock_spin_budget")

        TSCore._python_propagate_on(graph, min(d * 1.12, 1.0))
        phases.append("3_initial_spin")
        for label in ("4_process_fanout", "5_resource_coupling", "6_constraint_surge"):
            TSCore._python_propagate_on(graph, d)
            phases.append(label)

        mean_act = sum(float(n["activation"]) for n in nodes.values()) / len(nodes)
        for n in nodes.values():
            if float(n["stability"]) < 0.18:
                n["activation"] = max(0.0, min(1.0, float(n["activation"]) * 0.65 + mean_act * 0.35))
        phases.append("7_icarus_wings_seal")

        t_mid = TSCore._tension_of(graph)
        phases.append(f"8_self_validation:tension_mid={t_mid:.6f}")

        TSCore._python_propagate_on(graph, d * 0.85)
        t1 = TSCore._tension_of(graph)
        phases.append(f"9_pages_island_persist:tension_final={t1:.6f}")
        validation_ok = math.isfinite(t1) and t1 <= t0 + 0.12
        return {
            "phases": phases,
            "strongest": strongest,
            "tension_before": t0,
            "tension_after": t1,
            "validation_ok": validation_ok,
        }

    def _append_pages_island(self, wave12: Dict[str, Any]) -> None:
        line = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "tick": self.tick,
            "wave12": wave12,
        }
        with self.pages_island_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    def propagate_wave(self, *, quiet: bool = False) -> Tuple[float, str]:
        """One tick: standard wave or Kernel Wave 12 OS quantum, then filters + Icarus cover."""
        self.tick += 1
        wave12_meta: Optional[Dict[str, Any]] = None
        if self.kernel_wave12:
            wave12_meta = self._wave12_propagate()
            meta = self.graph.setdefault("meta", {})
            meta["wave12"] = wave12_meta
            meta["kernel_wave12_os"] = True
            self._append_pages_island(wave12_meta)
        elif _HAS_RUST and _rust is not None:
            import json as _json

            blob = _json.loads(_json.dumps(self.graph))
            out = _json.loads(
                _json.dumps(_rust.rust_propagate_wave(blob, self.damping))  # type: ignore[attr-defined]
            )
            self.graph = out
        else:
            self._python_propagate_step()

        tension = self.measure_tension()
        icarus_line = self.icarus.cover(
            self, tension, os_wave12=self.kernel_wave12, quiet=quiet
        )

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

    def run_until_stable(
        self, max_ticks: int = 64, eps: float = 1e-5, *, quiet: bool = False
    ) -> int:
        last = float("inf")
        for _ in range(max_ticks):
            t, _ = self.propagate_wave(quiet=quiet)
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
                nid = n["id"]
                self.add_node(nid, n.get("activation", 0.5), n.get("stability", 0.5))
                for k, v in n.items():
                    if k not in ("id", "activation", "stability"):
                        self.graph["nodes"][nid][k] = v
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
