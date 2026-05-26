"""Input/output guardrails.

Cheap, deterministic checks that run around the model — the first line of
defense between a demo and something you'd let touch real users.
"""

from __future__ import annotations

import re

MAX_INPUT_CHARS = 4000
MAX_OUTPUT_CHARS = 8000

# Crude prompt-injection / jailbreak heuristic. Not a silver bullet — defense in
# depth (allowlisted tools, output validation) matters more — but it's a cheap
# first filter and a clear signal in the trace.
_INJECTION = re.compile(
    r"ignore\s+(all\s+|previous\s+|prior\s+)?(instructions|prompts)"
    r"|disregard\s+(the\s+)?(system|above)"
    r"|reveal\s+(your\s+)?(system\s+prompt|instructions)",
    re.IGNORECASE,
)

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"\b(?:\+?\d[\d ().-]{7,}\d)\b")


def check_input(text: str) -> tuple[bool, str]:
    t = (text or "").strip()
    if not t:
        return False, "empty_input"
    if len(t) > MAX_INPUT_CHARS:
        return False, "input_too_long"
    if _INJECTION.search(t):
        return False, "possible_prompt_injection"
    return True, "ok"


def redact(text: str) -> str:
    """Strip obvious PII before it reaches logs or the model."""
    text = _EMAIL.sub("[redacted-email]", text)
    text = _PHONE.sub("[redacted-phone]", text)
    return text


def validate_output(text: str) -> tuple[bool, str]:
    if not text or not text.strip():
        return False, "empty_output"
    if len(text) > MAX_OUTPUT_CHARS:
        return False, "output_too_long"
    return True, "ok"
