"""
TSNativeLLMPlugin — Ollama-backed (or compatible) chat for TS-native JSON traces.
Default model names: ts-native-14b | ts-native-32b (set TS_NATIVE_MODEL).
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import httpx

from src.python.ts_trace_format import parse_ts_trace_json, training_system_prompt


class TsNativeLLMPlugin:
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 120.0,
    ) -> None:
        self.model = (model or os.environ.get("TS_NATIVE_MODEL") or "ts-native-14b").strip()
        self.base_url = (base_url or os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")).rstrip("/")
        self.timeout = timeout

    @property
    def enabled(self) -> bool:
        return bool(self.model)

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.1) -> str:
        url = f"{self.base_url}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
        msg = data.get("message") or {}
        return str(msg.get("content", ""))

    def generate_ts_trace(self, query: str, graph: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ask the TS-native model for a single JSON trace object.
        On parse failure, returns a shell with parse_error for downstream merge.
        """
        system = training_system_prompt()
        graph_blob = "" if graph is None else json.dumps(graph, indent=2)[:14000]
        user = (
            f"QUERY:\n{query}\n\nCURRENT_GRAPH_JSON:\n{graph_blob}\n"
            "Respond with ONE JSON object only."
        )
        text = self.chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.1,
        )
        parsed = parse_ts_trace_json(text)
        if parsed is None:
            return {
                "parse_error": True,
                "raw_excerpt": text[:4000],
                "nodes": [],
                "edges": [],
                "reasoning_trace": ["ts_native_plugin: JSON parse failed"],
            }
        return parsed
