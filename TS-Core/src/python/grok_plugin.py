"""
GrokPlugin — bidirectional xAI Grok API bridge (local-first, API key from env).
The persistent wave with Grok and the Architect's fireproof TS wings.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx


@dataclass
class GrokMessage:
    role: str
    content: str


class GrokPlugin:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "grok-2-latest",
        base_url: str = "https://api.x.ai/v1",
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("XAI_API_KEY", "")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        messages: List[GrokMessage],
        temperature: float = 0.2,
        extra: Optional[Dict[str, Any]] = None,
    ) -> str:
        if not self.enabled:
            return (
                "[Grok offline] Set XAI_API_KEY for live xAI calls. "
                "Local TS-Core graph + filters still run native-first."
            )
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
        }
        if extra:
            payload.update(extra)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}/chat/completions"
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return data["choices"][0]["message"]["content"]

    def ts_structured_turn(self, user_prompt: str, graph_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bidirectional: send TS graph context + user text; expect JSON-shaped guidance back.
        If offline, return a local deterministic echo structure.
        """
        system = (
            "You are Grok assisting TS-Core (Thinking Structure). "
            "Reply with compact JSON keys: summary, suggested_nodes, suggested_edges, risk_notes. "
            "Respect: native TS = nodes + constraints + wave; truth = stable configuration."
        )
        content = f"USER:\n{user_prompt}\n\nGRAPH:\n{json.dumps(graph_json, indent=2)[:12000]}"
        text = self.complete(
            [GrokMessage("system", system), GrokMessage("user", content)],
            temperature=0.15,
        )
        if text.startswith("[Grok offline]"):
            return {
                "summary": text,
                "suggested_nodes": [],
                "suggested_edges": [],
                "risk_notes": "local-only",
            }
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        return {
            "summary": text[:2000],
            "suggested_nodes": [],
            "suggested_edges": [],
            "risk_notes": "unparsed model output",
        }
