"""The lead-response agent: a manual agentic loop over the Anthropic SDK.

A manual loop (rather than the auto tool-runner) is deliberate: booking is a
real side effect, so the application — not the SDK — should own when tools fire,
how they're logged, and where confirmation gates go in production.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import anthropic

from .backend import Backend
from .config import BusinessConfig
from .prompts import build_system_prompt
from .tools import TOOL_SCHEMAS, dispatch

DEFAULT_MODEL = os.environ.get("LEAD_AGENT_MODEL", "claude-opus-4-7")
DEFAULT_EFFORT = os.environ.get("LEAD_AGENT_EFFORT", "medium")
_MAX_TOOL_HOPS = 6


@dataclass
class ToolEvent:
    name: str
    input: dict
    result: str


@dataclass
class Turn:
    reply: str
    tool_events: list[ToolEvent] = field(default_factory=list)


class LeadAgent:
    def __init__(self, config: BusinessConfig, backend: Backend, *, model: str = DEFAULT_MODEL, client: anthropic.Anthropic | None = None):
        self.config = config
        self.backend = backend
        self.model = model
        self.client = client or anthropic.Anthropic()
        today = backend.now().strftime("%A, %B %d, %Y")
        self.system = [{
            "type": "text",
            "text": build_system_prompt(config, today),
            "cache_control": {"type": "ephemeral"},
        }]
        self.messages: list[dict] = []

    def respond(self, lead_message: str) -> Turn:
        """Feed one inbound lead message; run tools to completion; return the reply."""
        self.messages.append({"role": "user", "content": lead_message})
        tool_events: list[ToolEvent] = []

        for _ in range(_MAX_TOOL_HOPS):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self.system,
                tools=TOOL_SCHEMAS,
                output_config={"effort": DEFAULT_EFFORT},
                messages=self.messages,
            )
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                reply = "".join(b.text for b in response.content if b.type == "text").strip()
                return Turn(reply=reply, tool_events=tool_events)

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = dispatch(block.name, dict(block.input), self.backend)
                    tool_events.append(ToolEvent(name=block.name, input=dict(block.input), result=result))
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            self.messages.append({"role": "user", "content": tool_results})

        # Safety valve: too many tool hops in one turn.
        return Turn(
            reply="Let me get a team member to follow up with you shortly.",
            tool_events=tool_events,
        )
