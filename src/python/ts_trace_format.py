"""
TS trace JSON — shared parse/apply helpers for training data, native LLM plugin, and evaluation.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from src.python.core import TSCore


def parse_ts_trace_json(text: str) -> Optional[Dict[str, Any]]:
    """Extract first JSON object from model output."""
    if not text or not text.strip():
        return None
    s = text.strip()
    start = s.find("{")
    end = s.rfind("}") + 1
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(s[start:end])
    except json.JSONDecodeError:
        return None


def _norm_node(item: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None
    nid = item.get("id") or item.get("node_id")
    if nid is None:
        return None
    return {
        "id": str(nid),
        "activation": float(item.get("activation", 0.5)),
        "stability": float(item.get("stability", 0.5)),
        **{k: v for k, v in item.items() if k not in ("id", "node_id", "activation", "stability")},
    }


def _norm_edge(item: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None
    fr = item.get("from") or item.get("source")
    to = item.get("to") or item.get("target")
    if fr is None or to is None:
        return None
    return {"from": str(fr), "to": str(to), "weight": float(item.get("weight", 1.0))}


def apply_ts_trace_dict_to_core(
    core: TSCore,
    d: Dict[str, Any],
    *,
    replace_graph: bool = False,
) -> Tuple[List[str], List[str]]:
    """
    Merge nodes/edges from a trace dict into core.
    Returns (created_node_ids, skipped_reasons).
    """
    created: List[str] = []
    skipped: List[str] = []

    inner = d.get("final_stable_configuration")
    if isinstance(inner, dict) and ("nodes" in inner or "edges" in inner):
        d = inner

    raw_nodes = d.get("nodes") or d.get("suggested_nodes") or []
    raw_edges = d.get("edges") or d.get("suggested_edges") or []

    if isinstance(raw_nodes, dict):
        raw_nodes = [{"id": k, **(v if isinstance(v, dict) else {})} for k, v in raw_nodes.items()]

    if replace_graph:
        core.graph = {"nodes": {}, "edges": []}

    for item in raw_nodes:
        n = _norm_node(item)
        if not n:
            skipped.append("bad_node")
            continue
        nid = n.pop("id")
        act = float(n.pop("activation"))
        stab = float(n.pop("stability"))
        if nid not in core.graph["nodes"]:
            core.add_node(nid, act, stab)
            created.append(nid)
            for k, v in n.items():
                core.graph["nodes"][nid][k] = v
        else:
            node = core.graph["nodes"][nid]
            node["activation"] = act
            node["stability"] = stab
            for k, v in n.items():
                node[k] = v

    for item in raw_edges:
        e = _norm_edge(item)
        if not e:
            skipped.append("bad_edge")
            continue
        core.add_edge(e["from"], e["to"], e["weight"])

    return created, skipped


def stability_map(graph: Dict[str, Any]) -> Dict[str, float]:
    nodes = graph.get("nodes") or {}
    return {str(k): float(v.get("stability", 0)) for k, v in nodes.items()}


def mean_stability(graph: Dict[str, Any]) -> float:
    m = stability_map(graph)
    if not m:
        return 0.0
    return sum(m.values()) / len(m)


def narrative_illusion_caught(meta: Dict[str, Any]) -> bool:
    dream = str(meta.get("narrative_dream", "")).lower()
    risk = str(meta.get("perceived_risk", "")).lower()
    if "routed through dream" in dream or "dream layer" in dream:
        return True
    if "reframed" in risk and "perceived" in risk:
        return True
    return False


def icarus_enforcement_line(meta: Dict[str, Any]) -> bool:
    line = str(meta.get("icarus", ""))
    return bool(line) and "WINGS COVERED" in line


def wave12_complete(w12: Dict[str, Any]) -> bool:
    phases = w12.get("phases") or []
    if len(phases) < 9:
        return False
    if w12.get("validation_ok") is False:
        return False
    return True


def training_user_prompt(query: str) -> str:
    return (
        "TS-Native trace task.\n"
        "Given the query, describe the correct Thinking Structure reaction.\n"
        "After reasoning, the assistant must output ONE JSON object only "
        "(no markdown fences) with native TS fields.\n\n"
        f"QUERY:\n{query}\n"
    )


def training_system_prompt() -> str:
    return (
        "You are TS-Native. Output a single JSON object with these keys:\n"
        "- nodes_created: string[]\n"
        "- wave_history: object[] (tick, tension, phase, icarus, filters, wave12_validation_ok)\n"
        "- stability_map: object mapping node id -> float\n"
        "- fireproof_events: string[]\n"
        "- kernel_wave_phases: string[][] (9 phase labels per OS quantum when Wave 12 applies)\n"
        "- icarus_enforcements: string[] (one line per tick where Icarus covered wings)\n"
        "- reasoning_trace: string[]\n"
        "- nodes: {id, activation, stability}[] graph patch to apply\n"
        "- edges: {from, to, weight}[]\n"
        "- final_stable_configuration: { nodes: dict id->{...}, edges: [...] }\n"
        "Use only numeric stabilites in [0,1]. Fireproof nodes should reach stability >= 0.96 when evolved."
    )
