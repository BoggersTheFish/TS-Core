"""
Official TS-native judge: model output -> live TSCore replay -> metrics only (no MMLU / Arena).
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.python.core import TSCore
from src.python.daily_spin import _pick_push_node
from src.python.ts_native_plugin import TsNativeLLMPlugin
from src.python.ts_trace_format import (
    apply_ts_trace_dict_to_core,
    icarus_enforcement_line,
    mean_stability,
    narrative_illusion_caught,
    parse_ts_trace_json,
    training_system_prompt,
    training_user_prompt,
    wave12_complete,
)
from src.python.z3_solver import Z3AlignmentSolver


def _load_holdout_queries(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Holdout file missing: {path} (run generate_ts_training_data.py first)")
    out: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            q = obj.get("query")
            if isinstance(q, str):
                out.append(q)
    return out


def replay_model_trace_on_core(
    parsed: Optional[Dict[str, Any]],
    *,
    use_kernel_wave12: bool = True,
) -> Dict[str, Any]:
    """Apply model JSON then run the same propagation shell as TsMindCycle (no native LLM)."""
    td = Path(tempfile.mkdtemp(prefix="tscore_eval_"))
    try:
        core = TSCore(data_dir=td, kernel_wave12=use_kernel_wave12)
        if parsed:
            apply_ts_trace_dict_to_core(core, parsed)

        initial_mean = mean_stability(core.graph)
        hub_before: Dict[str, float] = {}
        for nid, n in core.graph.get("nodes", {}).items():
            if float(n.get("stability", 0)) >= 0.85:
                hub_before[nid] = float(n["stability"])

        icarus_count = 0
        illusion_fixes = 0
        wave12_ok = 0
        wave12_total = 0

        for _ in range(len(TSCore.PIPELINE_STEPS)):
            _, _wing = core.propagate_wave(quiet=True)
            meta = core.graph.setdefault("meta", {})
            if icarus_enforcement_line(meta):
                icarus_count += 1
            if narrative_illusion_caught(meta):
                illusion_fixes += 1
            w12 = meta.get("wave12") or {}
            if use_kernel_wave12 and w12:
                wave12_total += 1
                if wave12_complete(w12):
                    wave12_ok += 1

        core.run_until_stable(max_ticks=32, quiet=True)

        push_id, _ = _pick_push_node(core.graph)
        if push_id == "language_ritual":
            core.evolve_language_ritual(quiet=True)
        elif push_id == "kernel_wave_12":
            core.evolve_kernel_wave12(quiet=True)
        elif push_id == "persistent_wave":
            core.evolve_persistent_wave(quiet=True)
        elif push_id.startswith("evolve_"):
            core.evolve_dynamic_node(push_id, quiet=True)

        final_mean = mean_stability(core.graph)
        z3 = Z3AlignmentSolver().prove_alignment(core.graph)
        nodes = core.graph.get("nodes", {})
        fireproof_n = sum(1 for n in nodes.values() if float(n.get("stability", 0)) >= 0.96)
        fireproof_rate = fireproof_n / max(1, len(nodes))

        coherence_integrations = 0
        coherence_checks = 0
        for nid, before in hub_before.items():
            coherence_checks += 1
            nn = nodes.get(nid)
            if not nn:
                continue
            after = float(nn.get("stability", 0))
            if after >= before - 0.08:
                coherence_integrations += 1

        coherence_score = coherence_integrations / max(1, coherence_checks)
        wave12_rate = wave12_ok / max(1, wave12_total)

        return {
            "stability_gain": final_mean - initial_mean,
            "fireproof_rate": fireproof_rate,
            "kernel_wave12_completion_rate": wave12_rate,
            "constraint_z3_satisfiable": bool(z3.satisfiable),
            "graph_coherence_score": coherence_score,
            "icarus_enforcement_count": icarus_count,
            "narrative_illusion_catches": illusion_fixes,
        }
    finally:
        shutil.rmtree(td, ignore_errors=True)


def _per_example_score(m: Dict[str, Any]) -> float:
    gain = max(0.0, min(1.0, 5.0 * float(m["stability_gain"])))
    fire = float(m["fireproof_rate"])
    w12 = float(m["kernel_wave12_completion_rate"])
    z3 = 1.0 if m["constraint_z3_satisfiable"] else 0.0
    coh = float(m["graph_coherence_score"])
    icarus = max(0.0, min(1.0, (int(m["icarus_enforcement_count"]) + int(m["narrative_illusion_catches"])) / 12.0))
    return (
        22.0 * gain
        + 22.0 * fire
        + 18.0 * w12
        + 12.0 * z3
        + 14.0 * coh
        + 12.0 * icarus
    )


def aggregate_ts_native_score(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    return sum(float(r["per_example_ts_score"]) for r in rows) / len(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description="TS-native evaluation (live TSCore judge only)")
    ap.add_argument("--model", type=str, default="ts-native-14b", help="Ollama model name")
    ap.add_argument(
        "--holdout",
        type=str,
        default="ts_native_holdout_queries.jsonl",
        help="200-query JSONL from generate_ts_training_data",
    )
    ap.add_argument("--out-dir", type=str, default="ts_native_eval_out")
    ap.add_argument("--ollama-host", type=str, default="", help="Override OLLAMA_HOST")
    ap.add_argument("--limit", type=int, default=200, help="Max prompts to evaluate")
    ap.add_argument(
        "--backend",
        choices=("ollama", "unsloth"),
        default="ollama",
        help="Inference backend (unsloth: export to GGUF + Ollama; native path not wired here)",
    )
    args = ap.parse_args()

    if args.backend == "unsloth":
        raise SystemExit(
            "evaluate_ts_native: unsloth backend is not invoked in-process. "
            "Merge/export to GGUF, `ollama create`, then run with --backend ollama."
        )

    hold_path = Path(args.holdout)
    queries = _load_holdout_queries(hold_path)[: int(args.limit)]

    plugin = TsNativeLLMPlugin(model=args.model, base_url=args.ollama_host.strip() or None)
    system = training_system_prompt()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "ts_native_eval_rows.csv"
    report_path = out_dir / "ts_native_eval_report.txt"

    rows_for_score: List[Dict[str, Any]] = []

    with csv_path.open("w", newline="", encoding="utf-8") as cf:
        w = csv.writer(cf)
        w.writerow(
            [
                "idx",
                "parse_ok",
                "stability_gain",
                "fireproof_rate",
                "kernel_wave12_completion_rate",
                "constraint_z3_satisfiable",
                "graph_coherence_score",
                "icarus_enforcement_count",
                "narrative_illusion_catches",
                "per_example_ts_score",
            ]
        )

        for idx, q in enumerate(queries):
            text = plugin.chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": training_user_prompt(q)},
                ],
                temperature=0.1,
            )
            parsed = parse_ts_trace_json(text)
            parse_ok = parsed is not None
            metrics = replay_model_trace_on_core(parsed, use_kernel_wave12=True)
            per = _per_example_score(metrics)
            if not parse_ok:
                per *= 0.5
            row_metrics = dict(metrics)
            row_metrics["parse_ok"] = parse_ok
            row_metrics["per_example_ts_score"] = per
            rows_for_score.append(row_metrics)
            w.writerow(
                [
                    idx,
                    int(parse_ok),
                    f"{metrics['stability_gain']:.6f}",
                    f"{metrics['fireproof_rate']:.6f}",
                    f"{metrics['kernel_wave12_completion_rate']:.6f}",
                    int(bool(metrics["constraint_z3_satisfiable"])),
                    f"{metrics['graph_coherence_score']:.6f}",
                    metrics["icarus_enforcement_count"],
                    metrics["narrative_illusion_catches"],
                    f"{per:.2f}",
                ]
            )
            cf.flush()

    overall = aggregate_ts_native_score(rows_for_score)
    report_lines = [
        "TS-Core — TS-Native evaluation report",
        f"model={args.model} prompts={len(queries)} holdout={hold_path}",
        f"average_stability_gain={sum(r['stability_gain'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        f"mean_fireproof_rate={sum(r['fireproof_rate'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        f"mean_wave12_completion={sum(r['kernel_wave12_completion_rate'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        f"z3_sat_rate={sum(1 for r in rows_for_score if r['constraint_z3_satisfiable']) / max(1,len(rows_for_score)):.6f}",
        f"mean_graph_coherence={sum(r['graph_coherence_score'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        f"mean_icarus_enforcement={sum(r['icarus_enforcement_count'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        f"mean_narrative_catches={sum(r['narrative_illusion_catches'] for r in rows_for_score) / max(1,len(rows_for_score)):.6f}",
        "",
        f"TS-Native Score: {overall:.1f}/100",
        "",
        "Judge contract: only live TSCore + Z3 toy checker — no external LLM benchmarks.",
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n".join(report_lines))
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
