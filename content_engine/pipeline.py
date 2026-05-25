"""Article generation pipeline built on the Anthropic SDK."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

import anthropic

from .prompts import ARTICLE_SCHEMA, SYSTEM_PROMPT, build_brief

DEFAULT_MODEL = os.environ.get("CONTENT_ENGINE_MODEL", "claude-opus-4-7")

# USD per million tokens. Cache write = 1.25x input, cache read = 0.1x input.
_PRICING = {
    "claude-opus-4-7": (5.0, 25.0),
    "claude-opus-4-6": (5.0, 25.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}


@dataclass
class ArticleBrief:
    topic: str
    primary_keyword: str
    secondary_keywords: list[str] = field(default_factory=list)
    word_count: int = 1500
    tone: str = "clear, professional, helpful"
    audience: str = "general readers researching the topic"
    extra_notes: str = ""


@dataclass
class GenerationResult:
    data: dict
    usage: anthropic.types.Usage
    model: str

    @property
    def estimated_cost_usd(self) -> float:
        in_rate, out_rate = _PRICING.get(self.model, (5.0, 25.0))
        u = self.usage
        cached_write = getattr(u, "cache_creation_input_tokens", 0) or 0
        cached_read = getattr(u, "cache_read_input_tokens", 0) or 0
        cost = (
            u.input_tokens * in_rate
            + cached_write * in_rate * 1.25
            + cached_read * in_rate * 0.1
            + u.output_tokens * out_rate
        ) / 1_000_000
        return round(cost, 4)


def generate_article(brief: ArticleBrief, *, model: str = DEFAULT_MODEL, client: anthropic.Anthropic | None = None) -> GenerationResult:
    """Generate a full SEO article package for the given brief.

    Streams the response (large outputs would otherwise risk an HTTP timeout)
    and returns the parsed JSON plus token usage for cost reporting.
    """
    client = client or anthropic.Anthropic()
    user_message = build_brief(
        topic=brief.topic,
        primary_keyword=brief.primary_keyword,
        secondary_keywords=brief.secondary_keywords,
        word_count=brief.word_count,
        tone=brief.tone,
        audience=brief.audience,
        extra_notes=brief.extra_notes,
    )

    with client.messages.stream(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={
            "effort": "high",
            "format": {"type": "json_schema", "schema": ARTICLE_SCHEMA},
        },
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        message = stream.get_final_message()

    text = next((b.text for b in message.content if b.type == "text"), None)
    if text is None:
        raise RuntimeError(f"No text content in response (stop_reason={message.stop_reason}).")

    data = json.loads(text)
    return GenerationResult(data=data, usage=message.usage, model=model)
