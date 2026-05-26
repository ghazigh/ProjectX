"""Structured tracing.

Every step the agent takes is recorded as an event. Without this you cannot
debug, evaluate, or audit an agent in production — you're flying blind.
"""

from __future__ import annotations

import json
import time
from collections import Counter


class Tracer:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self._t0 = time.monotonic()

    def event(self, type: str, **data) -> None:
        self.events.append({"t_ms": round((time.monotonic() - self._t0) * 1000), "type": type, **data})

    def tools_used(self) -> list[str]:
        return [e["name"] for e in self.events if e["type"] == "tool_call" and e.get("allowed")]

    def summary(self) -> dict:
        by_type = dict(Counter(e["type"] for e in self.events))
        model = [e for e in self.events if e["type"] == "model_request"]
        return {
            "events": len(self.events),
            "by_type": by_type,
            "model_calls": len(model),
            "tool_calls": sum(1 for e in self.events if e["type"] == "tool_call"),
            "input_tokens": sum(e.get("input_tokens", 0) for e in model),
            "output_tokens": sum(e.get("output_tokens", 0) for e in model),
        }

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(e) for e in self.events)

    def write(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_jsonl())
