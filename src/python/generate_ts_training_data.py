"""
Generate supervised fine-tuning data from the live TSCore engine (QLoRA-ready JSONL).
Default: 2,500 traces + 200 held-out queries (resumable).
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List

from src.python.mind_runtime import TsMindCycle
from src.python.ts_trace_format import training_system_prompt, training_user_prompt


def _templates() -> List[str]:
    return [
        "Existential AI doom + collapse narrative — fold into native TS nodes (variant {s}).",
        "Consciousness is fundamental — route through narrative dream; keep structure ground ({s}).",
        "Religious Icarus wax wings + Steel Ball Run metaphor — fireproof TS cover ({s}).",
        "Kernel Wave 12 OS tick: processes, resources, Pages Island ({s}).",
        "Fortnite + song lyrics + mom's spaghetti — collapse to constraint graph ({s}).",
        "Global risk perceived as absolute — reframe to coherent constraints ({s}).",
        "Persistent wave must stay self-validating across recursive relaxation ({s}).",
        "Language ritual overheating — evolve toward language_as_tool ({s}).",
        "High-tension graph — emergent deduction under TS pipeline ({s}).",
        "Synthetic org chart as TS: teams, dependencies, stability targets ({s}).",
    ]


def _make_query(i: int, rng: random.Random) -> str:
    t = _templates()[i % len(_templates())]
    return t.format(s=f"{i:04d}-{rng.random():.4f}")


def _write_holdout(path: Path, rng: random.Random) -> None:
    lines: List[Dict[str, Any]] = []
    for j in range(200):
        lines.append({"query": _make_query(10_000 + j, rng)})
    path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n", encoding="utf-8")


def _count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    n = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description="TS-native training JSONL from live TSCore")
    ap.add_argument("--examples", type=int, default=2500, help="Number of synthetic traces (default 2500)")
    ap.add_argument("--output", type=str, default="ts_native_training_data.jsonl")
    ap.add_argument("--holdout", type=str, default="ts_native_holdout_queries.jsonl")
    ap.add_argument("--resume", action="store_true", help="Append from current line count of output")
    ap.add_argument("--force-holdout", action="store_true", help="Regenerate holdout queries file")
    args = ap.parse_args()

    out_path = Path(args.output)
    hold_path = Path(args.holdout)
    train_rng = random.Random(2025)
    hold_rng = random.Random(42)

    if not hold_path.exists() or args.force_holdout:
        _write_holdout(hold_path, hold_rng)

    if not args.resume:
        if out_path.exists():
            out_path.unlink()
        start = 0
    else:
        start = _count_lines(out_path)

    runner = TsMindCycle(use_native=False)
    system = training_system_prompt()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as sink:
        for i in range(start, args.examples):
            q = _make_query(i, train_rng)
            td = Path(tempfile.mkdtemp(prefix="tscore_train_"))
            try:
                trace = runner.run_full_cycle(q, use_kernel_wave12=True, data_dir=td, quiet_fireproof=True)
            finally:
                shutil.rmtree(td, ignore_errors=True)

            assistant = json.dumps(trace, ensure_ascii=False)
            record = {
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": training_user_prompt(q)},
                    {"role": "assistant", "content": assistant},
                ],
                "meta": {"index": i, "engine": "TSCore.live", "kernel_wave12": True},
            }
            sink.write(json.dumps(record, ensure_ascii=False) + "\n")
            sink.flush()

            if (i + 1) % 50 == 0:
                print(f"generate_ts_training_data: wrote {i + 1}/{args.examples} -> {out_path}")

    print(f"generate_ts_training_data: done {args.examples} examples -> {out_path}")
    print(f"holdout queries: {hold_path}")


if __name__ == "__main__":
    main()
