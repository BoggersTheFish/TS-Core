# TS-Core — Thinking System Graph Dynamics Kernel

**Lightweight, local-first graph engine** with wave propagation for the TS (Thinking System) architecture.

Python-first with optional **Rust acceleration** (PyO3). Designed as the reusable core for wave-based cognitive systems.

---

## Quick Start

```bash
git clone https://github.com/BoggersTheFish/TS-Core.git
cd TS-Core

python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run the TUI / mind runtime
python -m src.python.mind_runtime
```

Or use the daily grounding spin:
```bash
python -m src.python.daily_spin
```

---

## What It Does

- Maintains a graph of nodes (with activation + stability) and weighted edges
- Runs **wave propagation** cycles (standard + Kernel Wave 12 mode)
- Applies filter layers and narrative/Icarus voice overlays
- Persistent JSON + JSONL history
- Optional Z3 constraint solver for toy alignment checks
- Optional Grok/xAI plugin

---

## Key Modes

- **Standard wave propagation**
- **Kernel Wave 12** — advanced 9-phase strongest-node biased cycle
- **Daily Spin** — quiet grounding + lowest-stability push

---

## Part of the TS Ecosystem

- Powers graph dynamics for **BoggersTheAI** and **BoggersTheCIG**
- Foundation for **GOAT-TS** experiments
- Used in **TensionLM / bozo** training loops

---

## Philosophy

This repo implements the **mechanical substrate** of TS: constraint graphs + continuous wave dynamics that produce emergent stability.

The narrative and philosophical layers sit on top of the actual graph engine.

---

**Default branch**: `master`

**License**: MIT

**Status**: Stable kernel, actively used across the TS project
