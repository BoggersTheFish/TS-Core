"""
Optional Streamlit GUI for TS-Core — run: python -m streamlit run src/python/streamlit_app.py
"""

from __future__ import annotations

import json

import streamlit as st

from src.python.core import TSCore
from src.python.grok_plugin import GrokPlugin
from src.python.z3_solver import Z3AlignmentSolver


st.set_page_config(page_title="TS-Core", layout="wide")
st.title("TS-Core v1.0 — native TS wave (local-first)")

if "core" not in st.session_state:
    st.session_state.core = TSCore()

core: TSCore = st.session_state.core

ingest = st.text_area(
    "Ingest narrative (risks, consciousness, Icarus, lyrics…)",
    value="Existential AI doom. Consciousness is fundamental. Icarus religion. Lose yourself spaghetti mist.",
)
if st.button("Propagate + filters + Icarus cover"):
    core.graph.setdefault("meta", {})["ingest"] = ingest
    t, wing = core.propagate_wave()
    st.success(f"tension={t:.4f}")
    st.info(wing)

st.subheader("Graph")
st.json(core.graph)

if st.button("Z3 alignment proof"):
    r = Z3AlignmentSolver().prove_alignment(core.graph)
    st.write({"satisfiable": r.satisfiable, "note": r.note, "model": r.model_summary})

if st.button("Grok structured turn"):
    g = GrokPlugin()
    out = g.ts_structured_turn("Map ingest to TS nodes/edges JSON fields.", core.graph)
    st.json(out)
