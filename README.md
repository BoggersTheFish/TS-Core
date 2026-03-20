# TS-Core v1.0

## What this repository is (exactly)

**TS-Core** is a **local-first Python library and CLI** (optional **Rust** acceleration via PyO3) that implements a small **graph dynamics engine** with persistence hooks. It is **application software** you run on your machine — not a replacement for your operating system kernel.

Concretely, the code maintains a **JSON-serializable graph** of **nodes** (each with numeric **activation** and **stability**, plus arbitrary extra fields) and **weighted edges**. On each tick, `TSCore.propagate_wave()` updates activations by **blending each node toward a weighted average of its neighbors** (damped). An alternate mode, **Kernel Wave 12**, runs a **nine-phase variant** of that dynamics (strongest-node bias, extra propagation passes, tension checks) and logs metadata — still **entirely inside this process**, over **your TS graph**, not over real OS processes.

Alongside the numbers, several **Python filter modules** inspect the graph and tension and write **human-readable labels** into graph `meta` (e.g. perceived-risk framing, narrative routing, “logic forcing” copy). **IcarusWingsCover** adds a consistent console **voice** and manifesto-style lines. Those layers are **heuristic glue and metaphor**, not a proof that natural-language claims are “true” in the world.

**Persistence:** under `TSCORE_HOME` (default `~/.tscore`), the core reads/writes a **factory JSON** (`self_improving_factory.json`) and appends **JSONL** history (`wave_history.jsonl`, optional `daily_spin.jsonl`, `pages_island.jsonl` for Wave 12).

**Optional integrations:**

- **Grok / xAI** (`GrokPlugin`): HTTP chat completions when `XAI_API_KEY` is set; otherwise a **local stub** so demos do not fail offline.
- **Z3** (`Z3AlignmentSolver`): builds a **small, abstract** satisfiability sketch over the graph (booleans + bounded reals for stability). Useful as a **smoke test** that the toy constraints can be satisfied — **not** a formal proof of real-world alignment or semantics of arbitrary text.

**Interfaces:** Textual **TUI** (`tscore` / `python -m src.python.mind_runtime`), **daily grounding** (`tscore-daily` / `python -m src.python.daily_spin`), optional **Streamlit** UI, **Docker Compose**, and optional Unix **`scripts/agi`** launcher (see below).

---

## What it does (capabilities)

- Loads or bootstraps a **factory graph**, **self-validates** on startup (relaxation on a deep copy; notes in `meta["startup_validation"]`).
- **Propagates** waves (pure Python by default; **Rust** `rust_propagate_wave` / `rust_wave12_propagate` if the `ts_core_kernel` extension is built).
- Runs the **filter stack** and **Icarus cover** each tick; advances an internal **8-step pipeline cursor** (phase names for logging, not a separate solver).
- **Daily spin** settles the graph quietly, prints a **sensible outcome** line, picks the **lowest-stability** node as “push today,” optionally runs **fireproof evolution** hooks, and appends **one JSONL line**.
- **Kernel Wave 12** mode: 9-phase trace, **Pages Island** JSONL line per tick when enabled.
- **Tests** (`tests/alignment_test.py`) exercise propagation, filters, Z3 toy model, history writes, and Wave 12 paths.

---

## Thinking Structure (TS) — conceptual frame

**TS** (Thinking Structure), as described at **[boggersthefish.com](https://boggersthefish.com)**, is a **meta-framework**: systems as **constraints, waves, and emergent stability**. This repo **encodes a runnable slice** of that idea (graphs, propagation, persistence, narrative filters). It does **not** by itself instantiate “TS as the logic of all reality”; it is a **tool and demo kernel** you can grow.

Canonical remote: **[github.com/BoggersTheFish/TS-Core](https://github.com/BoggersTheFish/TS-Core)**.

---

## Current limitations (important)

| Area | Limitation |
|------|------------|
| **Scope** | In-process **simulation** over **your declared graph**. Not a host OS scheduler, hypervisor, or distributed system unless **you** wire it to one. |
| **Semantics** | **No** deep NLP or world model. Filters use **simple rules** and graph/tension context; output is **staged copy + meta**, not verified epistemology. |
| **Z3** | **Toy** mapping from graph shape to constraints. **SAT** means the sketch is satisfiable, **not** that external claims or missions are “proven safe.” |
| **Grok** | Optional **third-party API**; stub responses are placeholders. |
| **Default graph** | The shipped **seed factory** is **illustrative**. Real use requires **modeling** nodes, edges, and any domain semantics yourself. |
| **Rust** | **Optional**; Python path is the **portable default**. |

---

## How to expand it

- **Domain graphs:** Replace or grow `self_improving_factory.json` (or load from your own builder) with nodes/edges that mean something in **your** system (org, product, research DAG, etc.).
- **New behavior:** Add filters or hooks (`on_propagate`), or call `propagate_wave` from your app and read `graph["meta"]` / JSONL for **telemetry, CI gates, or UI**.
- **Stronger assurance:** Tighten or replace the **Z3** layer with models that match **your** actual constraints; use TS-Core as a **thin simulation shell** around a real verifier.
- **Performance:** Build **`ts_core_kernel`** (maturin / `cargo build --features python`) for faster propagation on large graphs.
- **Deployment:** Embed the library in a **web backend**, run **Docker** services, or connect **Grok** only where API use is acceptable.

---

## Repo layout

The project root is the folder that contains `pyproject.toml` and `Cargo.toml`.

```text
.
├── README.md
├── CHANGELOG.md
├── Cargo.toml
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── scripts/
│   ├── agi                      # optional one-word Unix launcher → tscore TUI
│   └── install-agi-launcher.sh  # installs ~/.local/bin/agi + PATH hooks
├── src/
│   ├── python/
│   │   ├── core.py
│   │   ├── grok_plugin.py
│   │   ├── z3_solver.py
│   │   ├── coherence_filter.py
│   │   ├── narrative_dream_filter.py
│   │   ├── logic_forcing_layer.py
│   │   ├── icarus_wings_cover.py
│   │   ├── daily_spin.py
│   │   ├── mind_runtime.py
│   │   └── streamlit_app.py
│   ├── rust/
│   │   ├── lib.rs
│   │   ├── kernel.rs
│   │   └── bindings.rs
│   └── shared/
│       └── wave_propagate.rs
├── tests/
│   └── alignment_test.py
└── docs/
    └── Kernel-Wave-12.md
```

---

## One-command setup (laptop)

```bash
cd /path/to/this/repo
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev,gui]"
```

### Optional: Unix `agi` launcher

From a Unix shell, you can install a short **`agi`** command that activates the repo venv and runs **`tscore`**:

```bash
bash scripts/install-agi-launcher.sh
# then: agi
```

Set **`TS_CORE`** if the repo is not at `$HOME/TS-Core`.

### Daily grounding

Appends one JSON line to **`~/.tscore/daily_spin.jsonl`**. Uses `TSCore.propagate_wave(quiet=True)` so Icarus lines stay quiet until the summary.

```bash
python -m src.python.daily_spin
```

After `pip install -e .`, **`tscore-daily`** runs the same module.

**Push target:** lowest-stability node (tie-break: lower activation). If that node matches a **fireproof evolution** rule, the matching **`evolve_*`** method runs, factory JSON is rewritten, and the printed push line uses **post-evolution** values.

| Node ID | Method | Effect (summary) |
|--------|--------|------------------|
| `language_ritual` | `evolve_language_ritual()` | `language_as_tool`, stability floor, `meta.language_fireproof` |
| `kernel_wave_12` | `evolve_kernel_wave12()` | `kernel_fireproof`, stability/activation floors |
| `persistent_wave` | `evolve_persistent_wave()` | `persistent_fireproof`, stability/activation floors |
| `evolve_*` | `evolve_dynamic_node(node_id)` | `evolved` flag, stability/activation floors |

### Run (terminal TUI)

```bash
python -m src.python.mind_runtime
# or: tscore
```

Demo (filters + Icarus + Z3 + Grok stub):

```bash
python -m src.python.mind_runtime --demo
```

### Optional Streamlit GUI

```bash
pip install -e ".[gui]"
python -m streamlit run src/python/streamlit_app.py
```

Docker Compose profile **`tscore-gui`** exposes port **8501**.

### Grok / xAI

```bash
set XAI_API_KEY=your_key   # Windows
export XAI_API_KEY=your_key  # Unix
```

### Tests

```bash
python -m pytest tests/alignment_test.py -v
```

**Kernel Wave 12:** `test_kernel_wave12_fireproof_os_stability` covers the 9-phase path, **`pages_island.jsonl`**, and related metadata.

### Quick verification

```bash
python -m pytest tests/alignment_test.py -v
python -m src.python.daily_spin
```

See **`CHANGELOG.md`** for a concise capability history.

---

## Rust kernel + Python bindings (optional)

```bash
cargo build --release
cargo build --release --features python
```

For the extension module, **[maturin](https://www.maturin.rs/)** is recommended. On bleeding-edge Python, `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` may be needed (see `.cargo/config.toml`).

---

## Docker / Compose

```bash
docker compose run --rm tscore
docker compose run --rm tscore-tui
docker compose --profile gui up tscore-gui
```

Data persists in volume **`tscore_data`** at `/data/tscore`.

---

## Kernel Wave 12 (Pages Island) — technical note

**Kernel Wave 12** is the **nine-phase strongest-node-biased propagation** path (`Wave12Scheduler` in `src/rust/kernel.rs`, mirrored in Python in `TSCore._python_wave12_propagate_blob`). It **simulates** an “OS quantum” over the **TS graph** (phase labels, tension before/after, optional **Icarus** kernel line). It does **not** schedule real CPU processes unless you **integrate** graph state with an external system.

```bash
pip install -e ".[dev]"
python -m src.python.mind_runtime --kernel-wave12
```

Or: `set TSCORE_KERNEL_WAVE12=1` (Windows) / `export TSCORE_KERNEL_WAVE12=1` (Unix).

Full narrative and snippets: **`docs/Kernel-Wave-12.md`**.

---

## Design voice (optional reading)

The codebase intentionally carries **Architect / BoggersTheFish** framing: perceived risk as **coherence-limited**, consciousness claims routed through **narrative dream**, **LogicForcingLayer** pinned axioms, and **IcarusWingsCover** as a metaphor for **language/myth vs constraint-grounded outcomes**. That is **product philosophy and logging style**, layered on top of the **mechanical** graph engine described at the top of this file.

---

## License

MIT — see intent to open publication with **[BoggersTheFish](https://github.com/BoggersTheFish)**.
