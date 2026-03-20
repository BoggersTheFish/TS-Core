# Changelog

All notable changes to **TS-Core** are documented here. The canonical remote is [github.com/BoggersTheFish/TS-Core](https://github.com/BoggersTheFish/TS-Core).

## [1.0.0+] — Current `main` / `kernel-wave-12`

### Daily grounding

- **`src/python/daily_spin` / `tscore-daily`**: quiet `propagate_wave(quiet=True)` settle ticks; one **sensible outcome** line combining all filters + Icarus perfection; **lowest-stability push** target; append-only **`daily_spin.jsonl`** under `TSCORE_HOME` (~/.tscore).
- **Evolution order**: select push node → run matching **fireproof evolve** if applicable → **refresh** activation/stability for the printed line → then print outcome + “Push today”.

### Fireproof node evolution (`TSCore`)

- **`evolve_language_ritual()`** — `language_as_tool`, stability floor, factory persist; integrates with **Icarus** (`language_fireproof`, optional evolution echo when not `quiet`).
- **`evolve_kernel_wave12()`** — `kernel_fireproof` default OS layer marker + meta.
- **`evolve_persistent_wave()`** — `persistent_fireproof` permanent wave marker + meta.
- **`evolve_dynamic_node(node_id)`** — any factory node id **`evolve_*`**: `evolved`, stability/activation floors, `meta.last_evolved`.

### Kernel Wave 12 (Pages Island)

- Rust **`Wave12Scheduler`** 9-phase OS quantum + PyO3 **`rust_wave12_propagate`**; Python mirror when extension absent.
- **`TSCore(kernel_wave12=True)`** / **`TSCORE_KERNEL_WAVE12`** / CLI **`--kernel-wave12`**.
- **`pages_island.jsonl`** per Wave-12 quantum.

### Core ergonomics

- **`propagate_wave(quiet=...)`**, **`run_until_stable(quiet=...)`** for silent batches.
- **Factory load** preserves arbitrary node fields (not only activation/stability) so evolution flags survive reloads.

### Proof / quality

- **`tests/alignment_test.py`**: full-stack narrative collapse, wave history JSONL, Kernel Wave 12 fireproof OS stability.

Run: `python -m pytest tests/alignment_test.py -v`
