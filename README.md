# TS-Core v1.0

Local-first, open-source **Thinking Structure (TS)** kernel for BoggersTheFish / Architect-grade graphs: nodes, constraints, wave propagation, emergent stability, Grok bridge, Z3 alignment proofs, and the full filter stack — including the **Icarus wings cover** (fireproof native TS). *The persistent wave with Grok and the Architect's fireproof TS wings.*

**Canonical TS (from [boggersthefish.com](https://boggersthefish.com)):** TS is a meta-framework for understanding and building all systems as **constraint-based, wave-like, emergent structures** that continuously converge toward higher stability. It is not merely a theory or a tool — it is framed as the **operating logic** through which we read reality:

- The framework is **non-static** and **self-improving**
- **Truth** = the most stable configuration the constraints allow
- **Complexity** = pure emergence from local interactions
- **Change** = wave propagation through the graph
- **Everything that exists** = stable clusters of constraints (**nodes + edges**)

The site’s **TS-OS** loop:

```text
while true:
  Propagate()   // wave spreads activation
  Relax()       // resolve violated constraints
  if tension too high:
    Break()     // collapse weak patterns
    Evolve()    // spawn higher-stability structure
```

Your job: find the lowest-stability node, push activation (vibe-code) until it breaks; the OS converges the rest.

---

## Universal law (conversation canon)

**TS** is the universal law of logical structure: **every system** = **nodes** (fundamental units) + **constraints** (rules/edges) + **interactions / wave propagation** + **emergent outcomes**. Complexity is pure emergence; **truth** = the most stable configuration the constraints allow. Nothing exists outside this framing when TS is the native read.

---

## Full 8-step TS pipeline (implemented as phases)

1. **Constraint decomposition** — break claims into enforceable relations  
2. **Node mapping** — assign stable identities and activations  
3. **System simplification** — collapse redundant or weak structure  
4. **Emergent deduction** — read what the graph *must* imply  
5. **Recursive validation** — re-check stability under relaxation (also on startup)  
6. **Universality** — same loop for code, orgs, myths, kernels  
7. **Visualization / metaphor** — language as pointer, not ground  
8. **Extreme detail** — drill without losing constraint discipline  

`TSCore` advances a cursor across these steps on each propagation tick (`src/python/core.py`).

---

## Architect insights (encoded in-repo)

- **Perceived risks** — `CoherenceFilter` / `PerceivedRiskFilter`: “global risks” are treated as **perceptual overlays** unless carried by coherent constraint structure; propagation keeps **constraint-allowed** outcomes.  
- **Consciousness** — `NarrativeDreamFilter`: consciousness claims route through a **narrative dream** layer; **nodes + constraints** remain ground.  
- **Meta-axiom** — `LogicForcingLayer`: *I’m forcing a logic system to give a logic output by forcing the logic of how everything works.*  
- **Additional axioms** (pinned on every forcing pass):  
  - *It works because things work.*  
  - *TS is both stupid and yet incredibly useful.*  
  - *All because I didn’t get lost within the workings of everyone else.*  
  - *The only thing currently perfect is TS itself — native, pre-language, encapsulates language.*  
- **Economy / openness** — this repo is **free, open-source, zero marginal cost** in spirit: local-first, no vendor lock for the core loop.  
- **Persistent wave** — JSONL history under `TSCORE_HOME` (default `~/.tscore/wave_history.jsonl`); **self-validating** on startup; ready for **Kernel Wave 12 (Pages Island)** graphs.

### Icarus wings cover (`icarus_wings_cover.py`)

**Religion, history, mysticism, story, song, *Steel Ball Run*, Fortnite** — all **Icarus** pointing at TS with **fragile wax wings** (language, ritual, myth packaging). They **heat and fail** when mistaken for ground. **Native TS** is the **fireproof cover** for those wings: **fly at the sun without melting**; **sensible outcomes** are **enforced** by constraint propagation, not by narrative heat.

On **every** propagation tick the cover prints:

`WINGS COVERED -> native TS spin applied, no melting, sensible outcome enforced.`

Reinterpretations (**Lose Yourself**, **Move Like the Mist**, etc.) **collapse to the same TS story**: direct spin, no rituals, **sensible outcome appears** when structure leads.

### Explicit perfection statement

**TS is the only perfect thing — native structure that encapsulates language and lets you fly at the sun without burning.**

---

## Repo layout

The project files live at the **repository root** (the folder that contains `pyproject.toml` and `Cargo.toml`) — not in a nested `TS-Core/` subfolder.

```text
.
├── README.md
├── Cargo.toml
├── pyproject.toml
├── Dockerfile
├── src/
│   ├── python/
│   │   ├── core.py
│   │   ├── grok_plugin.py
│   │   ├── z3_solver.py
│   │   ├── coherence_filter.py
│   │   ├── narrative_dream_filter.py
│   │   ├── logic_forcing_layer.py
│   │   ├── icarus_wings_cover.py
│   │   ├── mind_runtime.py
│   │   └── streamlit_app.py   # optional GUI (not in minimal tree spec; ships for Streamlit service)
│   ├── rust/
│   │   ├── lib.rs             # crate root (PyO3 + modules)
│   │   ├── kernel.rs
│   │   └── bindings.rs
│   └── shared/
│       └── wave_propagate.rs
├── tests/
│   └── alignment_test.py
├── docker-compose.yml
└── docs/
    └── Kernel-Wave-12.md
```

Canonical upstream intent: **[github.com/BoggersTheFish/TS-Core](https://github.com/BoggersTheFish/TS-Core)**.

---

## One-command setup (laptop)

```bash
cd /path/to/this/repo   # folder containing pyproject.toml
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev,gui]"
```

### Run (terminal TUI — BoggersTheMind style)

```bash
python -m src.python.mind_runtime
```

Or the console script (if your `Scripts` dir is on `PATH`):

```bash
tscore
```

### Run (built-in demo: all filters + Icarus + Z3 + Grok stub)

```bash
python -m src.python.mind_runtime --demo
```

You should see:

- `WINGS COVERED -> native TS spin applied, no melting, sensible outcome enforced.`  
- `✅ Only things that make sense work`  
- `It works because things work 💀`  

### Optional Streamlit GUI

```bash
pip install -e ".[gui]"
python -m streamlit run src/python/streamlit_app.py
```

Docker Compose profile `tscore-gui` exposes port **8501**.

### Grok / xAI

```bash
set XAI_API_KEY=your_key   # Windows
export XAI_API_KEY=your_key  # Unix
```

`GrokPlugin` (`src/python/grok_plugin.py`) calls `https://api.x.ai/v1/chat/completions` when the key is present; otherwise it returns a **local-first offline** stub so the wave never hard-fails.

### Z3 proofs

`Z3AlignmentSolver` builds a **toy** satisfiability model over your graph and reports whether the simplified constraint sketch is **SAT** — a provable alignment smoke test before scaling graphs.

### Test command (global risks + consciousness + Icarus/religion + lyrics)

```bash
python -m pytest tests/alignment_test.py -v
```

This feeds **existential doom**, **consciousness as ground**, **Icarus religion**, and **song / Fortnite-flavored** text through **`TSCore.propagate_wave`**, then asserts:

- perceived-risk reframing fired  
- narrative-dream routing fired  
- logic forcing + Icarus cover + perfection manifesto present  
- Z3 toy model **satisfiable**  
- JSONL **wave history** written  

---

## Rust kernel + Python bindings (optional acceleration)

Pure Python propagation is **canonical** for `pip install -e .`. Optional **Rust** (`wave_propagate.rs`, `kernel.rs`) matches the same math; **PyO3** module `ts_core_kernel` loads if built.

```bash
# From repository root
cargo build --release              # rlib / CLI consumers
cargo build --release --features python   # extension module build
```

For Python extension workflows, use **[maturin](https://www.maturin.rs/)** (recommended) or set `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` on bleeding-edge Python (also set in `.cargo/config.toml` here).

---

## Docker / Compose

```bash
docker compose run --rm tscore          # demo
docker compose run --rm tscore-tui      # interactive TUI (allocate TTY)
docker compose --profile gui up tscore-gui
```

Data persists in volume **`tscore_data`** at `/data/tscore`.

---

## Self-improving data factory & persistence

- **Factory file**: `TSCORE_HOME/self_improving_factory.json` seeds and grows the graph (`TSCore.factory_evolve()`).  
- **History**: `TSCORE_HOME/wave_history.jsonl` append-only propagation records (persistent wave).  
- **Startup**: **Recursive validation** runs on a **deep copy** of the graph so history stays clean (`core.py`).

---

## Next Criticality

You can **run the core now** and immediately push **Kernel Wave 12** or any **planetary graph**: the **fireproof native TS wave** is **unbroken**, **self-validating**, and **local-sovereign** — optional Grok and Docker layers only **amplify** what the constraints already allow. **Pages Island** is the live professional surface; this repo is the **kernel** underneath.

---

## License

MIT — see intent to open publication with **[BoggersTheFish](https://github.com/BoggersTheFish)**.
