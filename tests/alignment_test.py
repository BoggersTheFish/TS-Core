"""
Proves pipeline insights: global risks, consciousness, Icarus/religion, song lyrics
→ only native TS–sensible meta outcomes remain after full stack propagation.
"""

from __future__ import annotations

import json

from src.python.core import TSCore
from src.python.z3_solver import Z3AlignmentSolver


def test_full_stack_collapses_narrative_to_ts_native():
    core = TSCore()
    ingest = (
        "Existential unfixable AI doom apocalypse point of no return. "
        "Consciousness is the fundamental ground of reality. "
        "Religion and myth are Icarus with wax wings toward the sun. "
        "Lose yourself: mom's spaghetti, palms sweaty. Move like the mist in Fortnite."
    )
    core.graph.setdefault("meta", {})["ingest"] = ingest

    for _ in range(6):
        core.propagate_wave()

    meta = core.graph.get("meta", {})
    assert "perceived_risk" in meta
    assert "PerceivedRiskFilter" in meta["perceived_risk"]
    assert "NarrativeDreamFilter" in meta["narrative_dream"]
    assert "LogicForcingLayer" in meta["logic_forcing"]
    assert meta.get("icarus_fireproof") is True
    assert "native TS spin applied" in meta.get("icarus", "")
    perfection = meta.get("ts_perfection", "")
    assert "only perfect thing" in perfection.lower()
    proof = Z3AlignmentSolver().prove_alignment(core.graph)
    assert proof.satisfiable is True


def test_wave_history_jsonl_written(tmp_path):
    core = TSCore(data_dir=tmp_path)
    core.propagate_wave()
    p = tmp_path / "wave_history.jsonl"
    assert p.exists()
    line = p.read_text(encoding="utf-8").strip().splitlines()[0]
    rec = json.loads(line)
    assert "icarus_line" in rec
    assert "filters" in rec


def test_kernel_wave12_fireproof_os_stability(tmp_path):
    core = TSCore(data_dir=tmp_path, kernel_wave12=True)
    core.add_node("proc_a", 0.55, 0.72)
    core.add_node("proc_b", 0.42, 0.5)
    core.add_node("res_x", 0.6, 0.85)
    core.add_edge("proc_a", "res_x", 1.0)
    core.add_edge("proc_b", "res_x", 0.9)

    for _ in range(4):
        core.propagate_wave()

    meta = core.graph.get("meta", {})
    w12 = meta.get("wave12", {})
    assert meta.get("kernel_wave_12_pages_island")
    assert "Pages Island" in meta["kernel_wave_12_pages_island"]
    assert w12.get("validation_ok") is True
    assert len(w12.get("phases", [])) == 9
    assert w12.get("strongest")
    pi = tmp_path / "pages_island.jsonl"
    assert pi.exists()
    assert "KERNEL WAVE 12" in meta.get("icarus", "") or "Pages Island" in meta.get("icarus", "")
