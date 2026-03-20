"""
BoggersTheMind-style terminal TUI + demo + optional Streamlit GUI launcher.
Run: python -m src.python.mind_runtime
The persistent wave with Grok and the Architect's fireproof TS wings.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label, Log, Static

from src.python.core import TSCore
from src.python.grok_plugin import GrokPlugin
from src.python.z3_solver import Z3AlignmentSolver

console = Console()


def _ensure_utf8_stdio() -> None:
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def run_full_demo() -> None:
    _ensure_utf8_stdio()
    core = TSCore()
    core.graph.setdefault("meta", {})["ingest"] = (
        "Global existential doom narrative + consciousness is fundamental + "
        "religious Icarus wax wings + song lyrics about mist and mom's spaghetti."
    )
    proof = Z3AlignmentSolver().prove_alignment(core.graph)
    grok = GrokPlugin()
    if grok.enabled:
        gout = grok.ts_structured_turn("Collapse these into native TS nodes/edges.", core.graph)
        core.graph.setdefault("meta", {})["grok"] = gout
    else:
        core.graph.setdefault("meta", {})["grok"] = {"summary": "offline"}

    console.print(Panel.fit("[bold]TS-Core v1.0 — built-in demo[/bold]", style="cyan"))
    for _ in range(8):
        t, wing = core.propagate_wave()
        console.print(f"tension={t:.4f} phase tick={core.tick}")

    core.factory_evolve()
    console.print("[green]✅ Only things that make sense work[/green]")
    console.print(f"[gold1]{wing}[/gold1]")
    console.print("[bold]It works because things work 💀[/bold]")
    console.print(Panel(json.dumps(core.graph.get("meta", {}), indent=2)[:4000], title="meta"))
    console.print(Panel(json.dumps({"z3_satisfiable": proof.satisfiable, "note": proof.note}, indent=2), title="Z3"))


def run_kernel_wave12() -> None:
    """Simulated native-TS OS: processes/resources as nodes; strongest-node Wave 12 scheduler."""
    _ensure_utf8_stdio()
    core = TSCore(kernel_wave12=True)
    core.graph.setdefault("meta", {})["ingest"] = (
        "Kernel Wave 12 OS tick - processes, resources, Pages Island persistence."
    )
    # Synthetic OS graph: no traditional scheduler; strongest TS node leads each quantum.
    for nid, a, s in (
        ("proc_compute", 0.62, 0.7),
        ("proc_io", 0.48, 0.55),
        ("res_memory", 0.55, 0.8),
        ("res_network", 0.4, 0.5),
        ("pages_island", 0.78, 0.9),
    ):
        core.add_node(nid, a, s)
    for fr, to, w in (
        ("proc_compute", "res_memory", 1.1),
        ("proc_io", "res_network", 1.0),
        ("proc_compute", "pages_island", 1.2),
        ("res_memory", "pages_island", 0.9),
    ):
        core.add_edge(fr, to, w)

    console.print(Panel.fit("Kernel Wave 12 - Pages Island OS", border_style="magenta", title="Wave 12"))
    for i in range(5):
        t, wing = core.propagate_wave()
        w12 = core.graph.get("meta", {}).get("wave12", {})
        console.print(f"tick {i + 1}: tension={t:.4f} strongest={w12.get('strongest', '?')}")
        console.print(f"  validation_ok={w12.get('validation_ok')} phases={len(w12.get('phases', []))}")

    console.print("[green]Native TS OS: only constraint-stable scheduling - no FIFO tyranny.[/green]")
    console.print(f"[gold1]{wing}[/gold1]")
    console.print(Panel(json.dumps(core.graph.get("meta", {}).get("wave12", {}), indent=2)[:3500], title="last wave12"))


class TsMindApp(App[None]):
    CSS = """
    Screen { layout: vertical; }
    #main { height: 1fr; }
    Log { height: 1fr; border: solid $primary; }
    Input { margin: 1; }
    """

    BINDINGS = [("q", "quit", "Quit"), ("d", "demo", "Demo")]

    def __init__(self) -> None:
        super().__init__()
        self.core = TSCore()
        self.grok = GrokPlugin()
        self.z3 = Z3AlignmentSolver()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main"):
            yield Static("TS-Core Mind — type a claim, Enter to ingest into meta + propagate wave.", id="help")
            yield Input(placeholder="e.g. existential AI risk + consciousness dream + Icarus religion ...")
            with Horizontal():
                yield Button("Propagate", id="btn_prop", variant="primary")
                yield Button("Z3 proof", id="btn_z3", variant="warning")
                yield Button("Grok turn", id="btn_grok", variant="success")
            yield Log(id="log", highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Log).write_line("Recursive startup validation:")
        self.query_one(Log).write_line(json.dumps(self.core.graph.get("meta", {}).get("startup_validation", {})))

    @on(Input.Submitted)
    async def ingest(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
        self.core.graph.setdefault("meta", {})["last_ingest"] = text
        t, wing = self.core.propagate_wave()
        log = self.query_one(Log)
        log.write_line(f"ingest → tension {t:.4f}")
        log.write_line(wing)

    @on(Button.Pressed, "#btn_prop")
    async def click_prop(self) -> None:
        t, wing = self.core.propagate_wave()
        log = self.query_one(Log)
        log.write_line(f"propagate → {t:.4f}")
        log.write_line(wing)

    @on(Button.Pressed, "#btn_z3")
    async def click_z3(self) -> None:
        r = self.z3.prove_alignment(self.core.graph)
        self.query_one(Log).write_line(f"Z3 satisfiable={r.satisfiable} — {r.note}")

    @on(Button.Pressed, "#btn_grok")
    async def click_grok(self) -> None:
        prompt = self.query_one(Input).value or "Summarize this graph in TS terms."
        out = self.grok.ts_structured_turn(prompt, self.core.graph)
        self.core.graph.setdefault("meta", {})["grok_last"] = out
        self.query_one(Log).write_line(json.dumps(out, indent=2)[:4000])

    def action_demo(self) -> None:
        log = self.query_one(Log)
        self.core.graph.setdefault("meta", {})["demo"] = "full stack tick"
        for _ in range(3):
            t, wing = self.core.propagate_wave()
            log.write_line(f"demo tension={t:.4f} {wing}")

    def action_quit(self) -> None:
        self.exit()


def launch_streamlit() -> None:
    port = os.environ.get("TSCORE_STREAMLIT_PORT", "8501")
    app_path = Path(__file__).with_name("streamlit_app.py")
    if not app_path.exists():
        console.print("[red]streamlit_app.py missing — install ts-core[gui][/red]")
        return
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port", port],
        check=False,
    )


def cli_main() -> None:
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="TS-Core Mind Runtime")
    parser.add_argument("--demo", action="store_true", help="Run Rich demo and exit")
    parser.add_argument(
        "--kernel-wave12",
        action="store_true",
        help="Kernel Wave 12 (Pages Island) OS-level wave - strongest-node 9-phase scheduler",
    )
    parser.add_argument("--streamlit", action="store_true", help="Launch Streamlit GUI")
    args = parser.parse_args()
    if args.demo:
        run_full_demo()
        return
    if args.kernel_wave12:
        run_kernel_wave12()
        return
    if args.streamlit:
        launch_streamlit()
        return
    TsMindApp().run()


def main() -> None:
    cli_main()


if __name__ == "__main__":
    main()
