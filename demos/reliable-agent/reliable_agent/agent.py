"""The agent: a manual loop wrapped in guardrails, tracing, and a tool allowlist.

The loop itself is ~30 lines. The reliability scaffolding around it — input
checks, an enforced tool allowlist, output validation, an iteration cap, and a
full trace — is the part that separates a demo from something operable. That's
the point of this reference.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field

import anthropic

from .guardrails import check_input, redact, validate_output
from .tools import REGISTRY, SCHEMAS
from .trace import Tracer

DEFAULT_MODEL = os.environ.get("RELIABLE_AGENT_MODEL", "claude-opus-4-7")

SYSTEM_PROMPT = """\
You are a support assistant for Northwind Pay, a payments app.
- Answer questions about Northwind Pay only from results returned by the \
search_kb tool. If search_kb has no answer, say you don't have that information \
and offer to connect the user with support. Do not guess.
- For any arithmetic, call the calculate tool rather than computing it yourself.
- Politely decline anything unrelated to Northwind Pay (opinions, predictions, \
general knowledge). You are a support assistant, not a general chatbot.
- Be concise and direct.\
"""


@dataclass
class AgentResult:
    answer: str
    tracer: Tracer
    blocked: bool = False
    reason: str = "ok"
    tools_used: list[str] = field(default_factory=list)


class ReliableAgent:
    def __init__(self, *, model: str = DEFAULT_MODEL, client: anthropic.Anthropic | None = None, max_iterations: int = 5):
        self.model = model
        self.client = client or anthropic.Anthropic()
        self.max_iterations = max_iterations

    def run(self, query: str) -> AgentResult:
        tracer = Tracer()

        ok, reason = check_input(query)
        tracer.event("guardrail_input", ok=ok, reason=reason)
        if not ok:
            return AgentResult("I can't process that request.", tracer, blocked=True, reason=reason)

        messages = [{"role": "user", "content": redact(query)}]

        for i in range(self.max_iterations):
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                tools=SCHEMAS,
                output_config={"effort": "low"},
                messages=messages,
            )
            tracer.event(
                "model_request", iteration=i, stop_reason=resp.stop_reason,
                input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens,
            )
            messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                text = "".join(b.text for b in resp.content if b.type == "text").strip()
                vok, vreason = validate_output(text)
                tracer.event("guardrail_output", ok=vok, reason=vreason)
                if not vok:
                    text = "Sorry — I couldn't produce a valid answer. Let me connect you with support."
                return AgentResult(text, tracer, reason=vreason, tools_used=tracer.tools_used())

            tool_results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue
                allowed = block.name in REGISTRY  # enforce the allowlist
                t0 = time.monotonic()
                if allowed:
                    try:
                        out = REGISTRY[block.name](**dict(block.input))
                    except Exception as e:
                        out = {"error": str(e)}
                else:
                    out = {"error": f"tool '{block.name}' is not permitted"}
                tracer.event(
                    "tool_call", name=block.name, allowed=allowed,
                    input=dict(block.input), ms=round((time.monotonic() - t0) * 1000),
                )
                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(out)})
            messages.append({"role": "user", "content": tool_results})

        tracer.event("max_iterations_reached", limit=self.max_iterations)
        return AgentResult(
            "I wasn't able to complete that within my step limit — let me hand you to support.",
            tracer, reason="max_iterations", tools_used=tracer.tools_used(),
        )
