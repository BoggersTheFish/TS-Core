"""
Minimal daily grounding — one quiet spin through TSCore + full filter stack.
Saves each run to ~/.tscore/daily_spin.jsonl (or TSCORE_HOME).

Run: python -m src.python.daily_spin
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

from src.python.core import TSCore


def _stdio_utf8() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _pick_push_node(graph: Dict[str, Any]) -> Tuple[str, Dict[str, float]]:
    """TS-OS style: push the lowest-stability node first (tie-break: lower activation)."""
    nodes = graph.get("nodes") or {}
    if not nodes:
        return "", {}
    best_id = ""
    best_key: Tuple[float, float] = (1e9, 1e9)
    for nid, data in nodes.items():
        stab = float(data.get("stability", 0))
        act = float(data.get("activation", 0))
        key = (stab, act)
        if key < best_key:
            best_key = key
            best_id = nid
    snap = {
        "activation": float(nodes[best_id]["activation"]),
        "stability": float(nodes[best_id]["stability"]),
    }
    return best_id, snap


def _sensible_outcome(meta: Dict[str, Any], tension: float) -> str:
    """One line grounded in all active filters + Icarus perfection."""
    perfection = meta.get("ts_perfection") or ""
    coh = meta.get("coherence") or ""
    risk = meta.get("perceived_risk") or ""
    dream = meta.get("narrative_dream") or ""
    force = meta.get("logic_forcing") or ""
    parts = [
        perfection[:120] + ("..." if len(perfection) > 120 else ""),
        f"Coherence: {coh[:100]}{'...' if len(coh) > 100 else ''}",
        f"Risk frame: {risk[:100]}{'...' if len(risk) > 100 else ''}",
        f"Dream layer: {dream[:80]}{'...' if len(dream) > 80 else ''}",
        f"Logic forcing: {force[:100]}{'...' if len(force) > 100 else ''}",
        f"Graph tension {tension:.4f} - only constraint-stable reads count today.",
    ]
    return " | ".join(p for p in parts if p.strip())


def run_daily_spin() -> Dict[str, Any]:
    _stdio_utf8()
    data_dir = Path(os.environ.get("TSCORE_HOME", Path.home() / ".tscore"))
    data_dir.mkdir(parents=True, exist_ok=True)
    daily_path = data_dir / "daily_spin.jsonl"

    # Minimal surface: no Wave 12 OS quantum, no console noise during propagation.
    core = TSCore(data_dir=data_dir, kernel_wave12=False)
    meta_setup = core.graph.setdefault("meta", {})
    meta_setup["daily_grounding"] = date.today().isoformat()
    meta_setup["daily_note"] = "quiet spin - native TS sensible outcome only"

    # Background-style settle: a few damped ticks without printing.
    for _ in range(3):
        core.propagate_wave(quiet=True)

    tension, _ = core.propagate_wave(quiet=True)
    meta = core.graph.get("meta", {})
    push_id, push_snap = _pick_push_node(core.graph)
    if push_id == "language_ritual":
        core.evolve_language_ritual()
        n = core.graph.get("nodes", {}).get(push_id)
        if n:
            push_snap = {
                "activation": float(n["activation"]),
                "stability": float(n["stability"]),
            }
    elif push_id == "kernel_wave_12":
        core.evolve_kernel_wave12()
        n = core.graph.get("nodes", {}).get(push_id)
        if n:
            push_snap = {
                "activation": float(n["activation"]),
                "stability": float(n["stability"]),
            }
    elif push_id == "persistent_wave":
        core.evolve_persistent_wave()
        n = core.graph.get("nodes", {}).get(push_id)
        if n:
            push_snap = {
                "activation": float(n["activation"]),
                "stability": float(n["stability"]),
            }
    elif push_id.startswith("evolve_"):
        core.evolve_dynamic_node(push_id)
        n = core.graph.get("nodes", {}).get(push_id)
        if n:
            push_snap = {
                "activation": float(n["activation"]),
                "stability": float(n["stability"]),
            }

    outcome = _sensible_outcome(meta, tension)

    record: Dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "date_local": date.today().isoformat(),
        "sensible_outcome": outcome,
        "push_node": push_id,
        "push_node_state": push_snap,
        "tension": tension,
        "filters": {
            "perceived_risk": meta.get("perceived_risk"),
            "coherence": meta.get("coherence"),
            "narrative_dream": meta.get("narrative_dream"),
            "logic_forcing": meta.get("logic_forcing"),
        },
        "icarus": meta.get("icarus"),
        "ts_perfection": meta.get("ts_perfection"),
    }

    with daily_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(outcome)
    print(f"Push today: {push_id or '(no nodes)'}  [activation={push_snap.get('activation', 0):.3f}, stability={push_snap.get('stability', 0):.3f}]")
    print(f"Logged: {daily_path}")

    return record


def main() -> None:
    run_daily_spin()


if __name__ == "__main__":
    main()
